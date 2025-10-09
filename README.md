# DR2 Runbooks
This repository contains GitHub Actions workflows designed to execute runbook actions. 
These workflows help automate various tasks, particularly those related to operational recovery and mitigation in AWS environments.

## Overview
The primary purpose of this repository is to store and manage runbooks that can be executed through GitHub Actions. 
Runbooks are predefined sets of instructions to handle specific operational scenarios, such as isolating compromised code or remediating security incidents.

## Current Runbooks

### Remove NACL rules Runbook

The first action in this repository focuses on removing NACL rules from all NACLs for an account 
This action is intended to isolate our code in AWS in the event of compromised code or a security breach. 
By removing NACL rules, we effectively cut off network access, minimising the risk of further exploitation.

### Pause and resume Preservica activity

This will be used when Preservica is down for maintenance and upgrades. It invokes a lambda in [the ingest repository](https://github.com/nationalarchives/dr2-ingest/tree/main/python/lambdas/pause-preservica-activity)

## Infrastructure
The workflows require access to AWS. The roles and policies are defined in [the dr2-terrarform-environments repository](https://github.com/nationalarchives/dr2-terraform-environments/blob/main/runbooks.tf)
