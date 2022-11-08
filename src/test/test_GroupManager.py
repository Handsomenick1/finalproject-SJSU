import json
import sys
sys.path.append("../..")
import unittest
from unittest import mock
import boto3
import pytest
import json
from decimal import Decimal
import logging
from moto import mock_dynamodb, mock_lambda
from Lambda.GroupManager import startGroups_handler, startCompetition_handler, collectResult_handler
from aws_helper.DynamoDB import get_item_db, put_item_db, get_items_db
from test.TestData import roundData_startCompetition, roundData_startGroups, roundData_collectResult, eventMetaData, groupData
from test.Unittest import mock_some_lambda, lambda_getAvailableRooms, lambda_getAvailableJudges, lambda_normal
@mock_dynamodb
@mock_lambda
class test_GroupManager(unittest.TestCase):
        
    def test_startGroups_handler_happy(self):
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        lambda_client = boto3.client('lambda', region_name='us-east-1')
        mock_some_lambda(lambda_client,"getAvailableRooms", lambda_getAvailableRooms())
        mock_some_lambda(lambda_client,"getAvailableJudges", lambda_getAvailableJudges())
        mock_some_lambda(lambda_client,"useJudge", lambda_normal())
        mock_some_lambda(lambda_client,"startRoom", lambda_normal())

        table_name = 'test_event_table'
        event_table = dynamodb.create_table(TableName=table_name,
                KeySchema=[{'AttributeName': 'eventId','KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'eventId','AttributeType': 'S'}],
                ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5  
        })
        event_meta_data_file_name = '.test.eventMetaData.json'
        with open(event_meta_data_file_name) as data:
            event_meta_data = json.load(data, parse_float=Decimal)
        #event_data = eventMetaData()
        put_item_db(event_table, event_meta_data)
        
        table_name = 'test_round_table'
        round_table = dynamodb.create_table(TableName=table_name,
                KeySchema=[{'AttributeName': 'roundId','KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'roundId','AttributeType': 'S'}],
                ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5  
        })
        round_data = roundData_startGroups()
        put_item_db(round_table, round_data)
        
        table_name = 'test_group_table'
        group_table = dynamodb.create_table(TableName=table_name,
                KeySchema=[{'AttributeName': 'groupId','KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'groupId','AttributeType': 'S'}],
                ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5  
        })
        group_data = groupData()
        for group in group_data:
            put_item_db(group_table, group)
        
        
        event = {
            "body": {
                "roundId": round_data["roundId"],
                "eventId": event_meta_data["eventId"],
                "tournamentId": "tm1"
            }
        }
        response = startGroups_handler(event, "")
        result = get_item_db(round_table, "roundId", "2")
        logging.info(result)
        assert response["statusCode"] == 200
         
    """
    def test_startCompetition_handler_happy(self):
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        table_name = 'test_round_table'
        round_table = dynamodb.create_table(TableName=table_name,
                KeySchema=[{'AttributeName': 'roundId','KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'roundId','AttributeType': 'S'}],
                ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5  
        })
        round_data = roundData_startCompetition()
        put_item_db(round_table, round_data)
        table_name = 'test_group_table'
        group_table = dynamodb.create_table(TableName=table_name,
                KeySchema=[{'AttributeName': 'groupId','KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'groupId','AttributeType': 'S'}],
                ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5  
        })
        group_data = groupData()
        put_item_db(group_table, group_data)
        event = {
            'roundId' : round_data["roundId"],
            'groupId' : group_data["groupId"]
            
        }
        response = startCompetition_handler(event, "")
        result = get_item_db(round_table, "roundId", "000001")
        assert response["statusCode"] == 200
        assert result["ASSIGNED"][0] == group_data
        
    def test_collectResult_handler(self):
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        lambda_client = boto3.client('lambda', region_name='us-east-1')
        mock_some_lambda(lambda_client,"finishRoom", lambda_event())
        mock_some_lambda(lambda_client,"startRoom", lambda_event())
        mock_some_lambda(lambda_client,"completeRound", lambda_event())
        
        table_name = 'test_round_table'
        round_table = dynamodb.create_table(TableName=table_name,
                KeySchema=[{'AttributeName': 'roundId','KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'roundId','AttributeType': 'S'}],
                ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5  
        })
        round_data = roundData_collectResult()
        put_item_db(round_table, round_data)
        
        table_name = 'test_group_table'
        group_table = dynamodb.create_table(TableName=table_name,
                KeySchema=[{'AttributeName': 'groupId','KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'groupId','AttributeType': 'S'}],
                ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5  
        })
        group_data = groupData()
        put_item_db(group_table, group_data)
        
        event = {
            'roundId' : round_data["roundId"],
            'groupId' : group_data["groupId"],
            'roomId' : 'abcroomd',
            'judgeingresult' : {
                    'judge1' : {
                        'score' : '99',
                        'note' : 'good'
                    },
                    'judge2' : {
                        'score' : '96',
                        'note' : 'good'
                    }
                }

        }
        
        response = collectResult_handler(event, "")
        db_result = get_item_db(group_table, "groupId", "group001")
        body = json.loads(response["body"])
        assert response["statusCode"] == 200
        assert body["message"] == "completed"
        assert db_result["judgeingresult"] == {
                    'judge1' : {
                        'score' : '99',
                        'note' : 'good'
                    },
                    'judge2' : {
                        'score' : '96',
                        'note' : 'good'
                    }
                }
"""