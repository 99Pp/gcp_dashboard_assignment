# Multi-Tenant Performance Visualization in Cloud Environments

## Project Overview

This project aims to monitor, process, and visualize performance metrics for multiple tenants in a cloud environment. The system collects, processes, and visualizes performance data to identify bottlenecks and optimize resource allocation. This is achieved using various Google Cloud Platform (GCP) services, including Google Cloud Monitoring, Pub/Sub, Dataflow, BigQuery, and Data Studio.

## Table of Contents

1. [Introduction](#introduction)
2. [Architecture](#architecture)
3. [Setup and Installation](#setup-and-installation)
4. [Data Collection](#data-collection)
5. [Data Processing](#data-processing)
6. [Data Visualization](#data-visualization)


## Introduction

Cloud providers need to monitor and optimize the performance of multi-tenant environments to ensure fair resource allocation and maintain quality of service. This project collects performance metrics such as CPU utilization, processes the data, and visualizes it to help cloud administrators identify and mitigate performance bottlenecks and optimize resource usage.

## Architecture

The architecture of this project involves the following components:

1. **Data Collection**: Collect performance metrics from Google Cloud Monitoring.
2. **Data Processing**: Process and transform the collected data using Google Cloud Dataflow.
3. **Data Storage**: Store the processed data in Google BigQuery.
4. **Data Visualization**: Visualize the data using Google Data Studio and a Flask web application.

### High-Level Architecture Diagram

![Architecture Diagram](link-to-architecture-diagram)

## Setup and Installation

### Prerequisites

- Google Cloud Platform account
- Python 3.7 or higher
- Google Cloud SDK (`gcloud`)
- Google Cloud Monitoring API enabled
- Google Cloud Pub/Sub API enabled
- Google Cloud Dataflow API enabled
- Google Cloud BigQuery API enabled

### Installation Steps

1. **Clone the Repository**
   ```
   git clone <this git link>
   cd multi-tenant-performance-visualization
2. **Set Up Google Cloud SDK**
   ```
   gcloud init
   gcloud auth application-default login
3. **Install Python Dependencies**
   ```
   pip install -r requirements.txt
4. **Set Environment Variable for Service Account**
   ```
   set GOOGLE_APPLICATION_CREDENTIALS=path\to\your\service-account-file.json
4. **Install Python Dependencies**
   ```
   Follow Design Document for detailed steps
