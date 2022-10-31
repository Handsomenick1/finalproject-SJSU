import sys 
sys.path.append("..")
import pytest
import unittest
import boto3
from moto import mock_dynamodb2
from Lambda.GroupManager import startGroups_handler, startCompetition_handler, collectResult_handler
from aws_helper.DynamoDB import put_item_db

@mock_dynamodb2
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
        round_data = {
            'roundId' : '000001',
            'QUEUED' : [],
            'ASSIGNED': [
                {'groupId': 'group001',
                 'roomId' : 'abcroomd',
                 'judgesIds': ['aaa', 'bbb'],
                 'competitorIds': ['c1', 'c2','c3'],
                 'result': {
                     
                 }}
                ],
            'STARTED' : [],
            'COMPLETED': []
        }
        put_item_db(round_table, round_data)
        table_name = 'test_group_table'
        group_table = dynamodb.create_table(TableName=table_name,
                KeySchema=[{'AttributeName': 'groupId','KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'groupId','AttributeType': 'S'}],
                ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5  
        })
        group_data = {'groupId': 'group001',
                 'roomId' : 'abcroomd',
                 'judgesIds': ['aaa', 'bbb'],
                 'competitorIds': ['c1', 'c2','c3'],
                 'result': {
                     
                 }}
        put_item_db(group_table, group_data)
        event = {
            'roundId' : '000001',
            'groupId' : 'group001'
            
        }
        response = startCompetition_handler(event, "")
        assert response["statusCode"] == 200