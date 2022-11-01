import sys
sys.path.append("..")
import unittest
import boto3
import pytest
from moto import mock_dynamodb
from Lambda.GroupManager import startGroups_handler, startCompetition_handler, collectResult_handler
from aws_helper.DynamoDB import get_item_db, put_item_db
from test.TestData import roundData, groupData

@mock_dynamodb
class test_GroupManager(unittest.TestCase): 
    #def test_startGroups_handler_happy(self):
        #dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        #table_name = 'test_table'
        
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
        round_data = roundData()
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