#!/usr/bin/env python3
import aws_cdk as cdk
from cdk.data_ingest_stack-rgn import DataIngestStack

# define some vars for tagging
org = 'SMF'
version = '1.1'
owner = 'dxc'
project = 'sdk-integration'
team = 'dev'

stack_name = project + '-' + team + '-data-ingest'

# init stack
app = cdk.App()
dataIngestStack = DataIngestStack(app, stack_name)

# apply tags
cdk.Tags.of(dataIngestStack).add("Organisation", org, apply_to_launched_instances=True)
cdk.Tags.of(dataIngestStack).add("Version", version, apply_to_launched_instances=True)
cdk.Tags.of(dataIngestStack).add("Owner", owner, apply_to_launched_instances=True)
cdk.Tags.of(dataIngestStack).add("Project", project, apply_to_launched_instances=True)
cdk.Tags.of(dataIngestStack).add("Team", team, apply_to_launched_instances=True)

# synth app
app.synth()
