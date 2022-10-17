import { Stack } from 'aws-cdk-lib';
import { Function } from 'aws-cdk-lib/aws-lambda';
import { createLogGroup } from './cloudwatch';
import * as tasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import * as stepfn from 'aws-cdk-lib/aws-stepfunctions'

export interface mainProps {
    example_lambda: Function
}

export function workflow(stack: Stack, props: mainProps) {

    // initialize state
    const state_pass = new stepfn.Pass(stack, "pass name");
    const state_fail = new stepfn.Fail(stack, "fail name");

    // initialize lambda function
    const example_handler = new tasks.LambdaInvoke(stack, "exampleHandler", {
        lambdaFunction: props.example_lambda
    });

    // initialize choice
    let choice_example = new stepfn.Choice(stack, "choice_example?", {
        comment: "example of comment"
    }).when(stepfn.Condition.booleanEquals(`$.isexample`, true), state_fail)
    .otherwise(state_pass);

    // connect work blocks
    const definition = example_handler.next(state_pass);
    definition.next(choice_example)

    
    return new stepfn.StateMachine(stack, "name of stepfn", {
        definition: definition,
        stateMachineName: "name of stepfn",
        logs: {
            destination: createLogGroup(stack, "name of stepfn")
        }
    })
}