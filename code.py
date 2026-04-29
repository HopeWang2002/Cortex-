import json
import time
import random

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def log(self, message, color=Colors.OKCYAN):
        print(f"{color}[{self.name} - {self.role}]{Colors.ENDC} {message}")

class PlannerAgent(Agent):
    def plan(self, requirement):
        self.log(f"正在拆解需求: {requirement}...", Colors.HEADER)
        time.sleep(1.5)
        # 模拟思维链 (CoT)
        tasks = [
            {"id": 1, "task": "设计后端 API 数据结构", "status": "pending"},
            {"id": 2, "task": "实现 React 前端审核页面组件", "status": "pending"},
            {"id": 3, "task": "集成单元测试用例", "status": "pending"}
        ]
        self.log(f"CoT 拆解完成，共生成 {len(tasks)} 个子任务。")
        return tasks

class CoderAgent(Agent):
    def generate_code(self, task, context=None, retry_count=0):
        action = "重新生成" if retry_count > 0 else "开始编写"
        self.log(f"{action}代码任务: {task['task']}...")
        time.sleep(2)
        
        # 模拟生成的代码片段
        mock_code = f"""
        // Generated Code for {task['task']}
        function processOrder(orderId) {{
            console.log("Processing order: " + orderId);
            // 模拟一个潜在的 Bug（在重试前）
            if (Math.random() > 0.7 && {retry_count} == 0) {{
                 throw new Error("Unexpected null pointer in order flow");
            }}
            return {{ status: 200, data: "Success" }};
        }}
        """
        self.log("代码生成完成。", Colors.OKGREEN)
        return mock_code

class QAAgent(Agent):
    def verify(self, code):
        self.log("正在执行单元测试与 Lint 检查...")
        time.sleep(1.5)
        
        # 模拟测试过程
        is_success = "Error" not in code or random.random() > 0.5
        if is_success:
            self.log("测试通过！代码已达到发布标准。", Colors.OKGREEN)
            return True, None
        else:
            error_msg = "Test failed: ReferenceError: orderId is not defined at line 4"
            self.log(f"发现异常: {error_msg}", Colors.FAIL)
            return False, error_msg

class AgentOrchestrator:
    def __init__(self):
        self.planner = PlannerAgent("Alice", "需求架构师")
        self.coder = CoderAgent("Bob", "全栈开发工程师")
        self.qa = QAAgent("Charlie", "测试审计员")
        self.total_tokens_simulated = 0

    def run(self, requirement):
        print(f"{Colors.BOLD}>>> 启动多 Agent 协作工作流...{Colors.ENDC}\n")
        
        # 1. 需求拆解
        tasks = self.planner.plan(requirement)
        self.total_tokens_simulated += 15000  # 模拟 CoT 消耗
        
        # 2. 迭代执行任务
        for task in tasks:
            print("-" * 50)
            verified = False
            retries = 0
            
            while not verified and retries < 3:
                # 编码
                code = self.coder.generate_code(task, retry_count=retries)
                self.total_tokens_simulated += 80000  # 模拟代码生成消耗
                
                # 验证
                success, error = self.qa.verify(code)
                self.total_tokens_simulated += 20000  # 模拟审计消耗
                
                if success:
                    verified = True
                    task["status"] = "completed"
                else:
                    retries += 1
                    self.coder.log(f"收到错误反馈，准备第 {retries} 次自我修复...", Colors.WARNING)
        
        print("\n" + "=" * 50)
        print(f"{Colors.OKGREEN}{Colors.BOLD}项目交付成功！{Colors.ENDC}")
        print(f"总预估 Token 消耗: {Colors.HEADER}{self.total_tokens_simulated}{Colors.ENDC}")
        print(f"交付周期缩短评价: {Colors.OKBLUE}优 (基于仿真环境){Colors.ENDC}")

if __name__ == "__main__":
    orchestrator = AgentOrchestrator()
    orchestrator.run("开发一个具有多级审核功能的订单管理模块")