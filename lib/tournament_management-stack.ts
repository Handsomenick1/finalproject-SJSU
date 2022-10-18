import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { createTable } from './resource/dynamodb';
import { workflow } from './resource/stepfunction';
import * as lambda from'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as cdk from 'aws-cdk-lib';
import * as path from 'path';
import { createSecret } from './resource/secret';

export class TournamentManagementStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

     // Example - dynamoDB
     const example_DB = createTable(this, 'TableName', 'PrimaryKey')

     // Example - lambda layer
     const examplelayer = new lambda.LayerVersion(this, 'layername', {
      compatibleRuntimes: [
        lambda.Runtime.PYTHON_3_7,
        lambda.Runtime.PYTHON_3_8
      ],
      code: lambda.Code.fromAsset('src/layer'),
      description: 'Layer descripton'
    })

    // Example - lambda function
    const example_lambda = new lambda.Function(this, 'firstHandler', {
      runtime: lambda.Runtime.PYTHON_3_7,
      timeout: cdk.Duration.seconds(6),
      code: lambda.Code.fromAsset(path.join(__dirname, `/../src/lambda`)), // where your lambda code located
      handler: 'RoundManager.lambda_handler', // file name . function name
      layers: [examplelayer],
      environment :{
        "region": this.region,
        'table' : example_DB.tableName
      }
    });

    // Example - Api gateway
    // == 1. initialize apigw == 
    const api = new apigateway.RestApi(this, 'temp-apigw', {
      description: 'example apigw',
      defaultCorsPreflightOptions:{
        allowHeaders: [
          'Content-Type',
          'X-Amz-Date',
          'Authorization',
          'X-Api-Key',
        ],
        allowMethods: ['OPTIONS', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
        allowCredentials: true,
        allowOrigins: ['http:// orignes that allow to make equests to this rest api'],
      }
    });
    new cdk.CfnOutput(this, 'apiUrl', {value: api.url});
    // == 2. add resource '/example' == 
    const example = api.root.addResource('example');
    // == 3. intergrate rescore with lambda function ==
    example.addMethod(
      'GET',
      new apigateway.LambdaIntegration(example_lambda, {proxy: true})
    )

    // Example - step function
    let mainProps = {
      example_lambda: example_lambda
    }
    const exampe_stepfn = workflow(this, mainProps)

    // Example - grant permission
    example_DB.grantFullAccess(example_lambda)
    exampe_stepfn.grantExecution(example_lambda)


    // Example - secret manager
    let secret = createSecret(this, "stage name")
  }
}
