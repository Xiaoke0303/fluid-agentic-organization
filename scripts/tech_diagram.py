#!/usr/bin/env python3
"""
Tech Diagram Generator - OpenClaw 版本
用自然语言描述生成技术架构图 (PNG/SVG)

依赖: diagrams, graphviz
"""

import sys
import argparse
from diagrams import Diagram, Cluster, Edge

# 基础组件
from diagrams.generic.blank import Blank
from diagrams.generic.network import Firewall
from diagrams.generic.compute import Rack
from diagrams.generic.place import Datacenter
from diagrams.generic.storage import Storage

# 编程语言和框架
from diagrams.programming.framework import FastAPI, Flask, Django, React, Vue, Angular
from diagrams.programming.language import Python, JavaScript, Go, Java, NodeJS

# 本地部署
from diagrams.onprem.database import PostgreSQL, MySQL, MongoDB, Cassandra
from diagrams.onprem.inmemory import Memcached, Redis
from diagrams.onprem.queue import Kafka, RabbitMQ
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx, Apache, Traefik
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Grafana, Prometheus

# 云服务 - AWS
from diagrams.aws.compute import EC2, Lambda, ECS, EKS
from diagrams.aws.database import RDS, Dynamodb, ElastiCache, Redshift
from diagrams.aws.network import ELB, CloudFront, Route53, APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS, SNS

# K8s
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.network import Service, Ingress
from diagrams.k8s.storage import PersistentVolume

# 简化的架构图生成器
def generate_rag_diagram(output_path="rag_architecture"):
    """生成 RAG 架构图"""
    with Diagram("RAG Pipeline Architecture", filename=output_path, show=False, direction="LR"):
        user = Server("User")
        
        with Cluster("Query Processing"):
            query = Server("Query Handler")
            embed = Server("Embedding Model")
            
        with Cluster("Retrieval"):
            vector_db = Redis("Vector DB")
            doc_store = MongoDB("Document Store")
            
        with Cluster("Generation"):
            llm = Server("LLM")
            context = Server("Context Builder")
            
        response = Server("Response")
        
        user >> query >> embed >> vector_db >> context >> llm >> response
        doc_store >> context

def generate_microservices_diagram(output_path="microservices_arch"):
    """生成微服务架构图"""
    with Diagram("Microservices Architecture", filename=output_path, show=False):
        lb = Nginx("Load Balancer")
        
        with Cluster("Service Mesh"):
            with Cluster("User Service"):
                user_api = FastAPI("User API")
                user_db = PostgreSQL("User DB")
                user_api >> user_db
                
            with Cluster("Order Service"):
                order_api = FastAPI("Order API")
                order_db = PostgreSQL("Order DB")
                order_api >> order_db
                
            with Cluster("Payment Service"):
                payment_api = FastAPI("Payment API")
                payment_queue = Kafka("Payment Queue")
                payment_api >> payment_queue
        
        with Cluster("Data Layer"):
            cache = Redis("Cache")
            message_bus = RabbitMQ("Event Bus")
        
        with Cluster("Monitoring"):
            prometheus = Prometheus("Metrics")
            grafana = Grafana("Dashboard")
        
        lb >> user_api
        lb >> order_api
        lb >> payment_api
        user_api >> cache
        order_api >> message_bus

def generate_multi_agent_diagram(output_path="multi_agent_system"):
    """生成多 Agent 系统架构图"""
    with Diagram("Multi-Agent System", filename=output_path, show=False, direction="TB"):
        user = Server("User")
        
        with Cluster("Orchestration Layer"):
            orchestrator = Server("Orchestrator")
            memory = Redis("Shared Memory")
            
        with Cluster("Specialist Agents"):
            search_agent = Server("Search Agent")
            code_agent = Server("Code Agent")
            review_agent = Server("Review Agent")
            
        with Cluster("Tools"):
            search_tool = Server("Search API")
            code_exec = Server("Code Executor")
            
        llm = Server("LLM Gateway")
        
        user >> orchestrator
        orchestrator >> memory
        orchestrator >> [search_agent, code_agent, review_agent]
        search_agent >> search_tool
        code_agent >> code_exec
        [search_agent, code_agent, review_agent] >> llm

def generate_mem0_diagram(output_path="mem0_architecture"):
    """生成 Mem0 记忆架构图"""
    with Diagram("Mem0 Memory Architecture", filename=output_path, show=False, direction="TB"):
        with Cluster("Input Layer"):
            user = Server("User")
            app = Server("AI App")
            client = Server("mem0 Client")
            
        with Cluster("Memory Manager"):
            manager = Server("Memory Manager")
            embed = Server("Embedding Model")
            
        with Cluster("Storage Tiers"):
            vector_db = Redis("Vector Store")
            graph_db = MongoDB("Graph DB")
            kv_store = Redis("KV Store")
            history = PostgreSQL("History Store")
            
        with Cluster("Output Layer"):
            context = Server("Context Builder")
            ranker = Server("Ranker")
            response = Server("Response")
            
        user >> app >> client >> manager
        manager >> embed
        manager >> [vector_db, graph_db, kv_store, history]
        [vector_db, graph_db, kv_store] >> context >> ranker >> response

def generate_data_pipeline_diagram(output_path="data_pipeline"):
    """生成数据管道架构图"""
    with Diagram("Data Pipeline", filename=output_path, show=False, direction="LR"):
        source = Server("Data Sources")
        
        with Cluster("Ingestion"):
            kafka = Kafka("Kafka")
            
        with Cluster("Processing"):
            spark = Server("Spark")
            
        with Cluster("Storage"):
            s3 = S3("Data Lake")
            warehouse = Redshift("Warehouse")
            
        with Cluster("Serving"):
            api = APIGateway("API Gateway")
            cache = ElastiCache("Cache")
            
        analytics = Grafana("Analytics")
        
        source >> kafka >> spark >> s3 >> warehouse >> api >> cache
        warehouse >> analytics

def generate_kubernetes_diagram(output_path="k8s_architecture"):
    """生成 Kubernetes 架构图"""
    with Diagram("Kubernetes Architecture", filename=output_path, show=False, direction="TB"):
        with Cluster("Control Plane"):
            api = Server("API Server")
            scheduler = Server("Scheduler")
            etcd = Server("etcd")
            
        with Cluster("Worker Nodes"):
            with Cluster("Node 1"):
                pod1 = Pod("App Pod")
                pod2 = Pod("Sidecar")
                svc1 = Service("Service")
                
            with Cluster("Node 2"):
                pod3 = Pod("App Pod")
                pod4 = Pod("Sidecar")
                svc2 = Service("Service")
                
        with Cluster("Storage"):
            pv = PersistentVolume("Persistent Volume")
            
        ingress = Ingress("Ingress")
        
        api >> scheduler
        api >> etcd
        ingress >> [svc1, svc2]
        svc1 >> [pod1, pod2]
        svc2 >> [pod3, pod4]
        [pod1, pod3] >> pv

# 主函数
def main():
    parser = argparse.ArgumentParser(description="Generate technical architecture diagrams")
    parser.add_argument("type", 
                       choices=["rag", "microservices", "multi-agent", "mem0", "data-pipeline", "kubernetes"],
                       help="Diagram type to generate")
    parser.add_argument("-o", "--output", default="diagram", help="Output filename (without extension)")
    parser.add_argument("-f", "--format", choices=["png", "svg", "pdf"], default="png",
                       help="Output format")
    
    args = parser.parse_args()
    
    generators = {
        "rag": generate_rag_diagram,
        "microservices": generate_microservices_diagram,
        "multi-agent": generate_multi_agent_diagram,
        "mem0": generate_mem0_diagram,
        "data-pipeline": generate_data_pipeline_diagram,
        "kubernetes": generate_kubernetes_diagram,
    }
    
    if args.type in generators:
        output = f"{args.output}"
        generators[args.type](output)
        print(f"Generated: {output}.png")
        
        # 如果请求 SVG 或 PDF，使用 graphviz 转换
        if args.format == "svg":
            import subprocess
            subprocess.run(["dot", "-Tsvg", f"{output}.png", "-o", f"{output}.svg"], check=False)
            print(f"Also generated: {output}.svg")
    else:
        print(f"Unknown diagram type: {args.type}")
        sys.exit(1)

if __name__ == "__main__":
    main()
