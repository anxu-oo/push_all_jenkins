import  jenkins
import  re,json,time,sys
server = jenkins.Jenkins('http://192.168.0.105:8080/',username='anxu',password='Abc...123')
# server = jenkins.Jenkins('http://jks.smarket.link/',username='anxu',password='Abc...123')
user = server.get_whoami()

version = server.get_version()
# print('Hello %s from Jenkins %s' % (user['fullName'], version))
#获取jenkins 视图
# view_config = server.get_view_config('test')
# views = server.get_views()
# print(views)

# def get_jobs(fordot):
#
#     def ta(task,l1):
#         if task["_class"]  == "com.cloudbees.hudson.plugins.folder.Folder":
#             l2 = l1 + "/" + task["name"]
#             for a in task["jobs"]:
#                 ta(a,l2)
#         else:
#             task_name = task["name"]
#             jobs_name = f"{l1}/{task_name}"
#             job_list.append(jobs_name)
#
#     #获取jenkins job
#     jobs = server.get_jobs()
#
#     l1 = fordot
#     for job in jobs:
#         if job["name"] == fordot:
#             for i in job["jobs"]:
#                 ta(i,l1)
#     return  job_list


# a = get_jobs("Smarket_K8sdemo")


# old_last_build_number = server.get_job_info('gh/nginx-jenkins')['lastBuild']['number']
# #
# server.build_job(name="gh/nginx-jenkins",parameters=arg)
# last_build_number = server.get_job_info('gh/nginx-jenkins')['lastBuild']['number']
# #
# while old_last_build_number == last_build_number:
#     print("任务未添加队列开始等待")
#     time.sleep(12)
#     last_build_number = server.get_job_info('gh/nginx-jenkins')['lastBuild']['number']
#
# #获取是否还在构建中
# # bulid_status = server.get_build_info('gh/nginx-jenkins', 56)['building']
# # print(bulid_status)
# #构建结束 SUCCESS|FAILURE<class 'str'>   ABORTED <class 'str'>  构建中None  None <class 'NoneType'>
# # while bulid_status != "False":
# #     print("未执行完开始等待")
# #     time.sleep(80)
# #     bulid_status = server.get_build_info('gh/nginx-jenkins', last_build_number)['building']
# # time.sleep(10)
# # print("结束等待")
# while True:
#
#     result = server.get_build_console_output(name='gh/nginx-jenkins', number=last_build_number)
#     print(result)
#     # if not re.match('Finished: SUCCESS',result) or not re.match("Finished: FAILURE",result):
#     if  re.search('Finished',result):
#         break
#     time.sleep(10)



# status = server.get_build_info('gh/nginx-jenkins', last_build_number)['result']
# print(status)
# last_build_info=server.get_job_info('gh/nginx-jenkins')
# last_success_build_number = last_build_info['lastSuccessfulBuild']['number']
# laste_build_number = last_build_info['lastBuild']['number']
# #最后一次失败
# laste_unsuccess_build_number = last_build_info['lastUnsuccessfulBuild']['number']
# #获取最近成功的一次
# last_unstable_build = last_build_info['lastStableBuild']['number']
# builds = last_build_info['builds']  # 获取job所有的build历史记录
# print("\n","\n","\n",last_unstable_build,"\n")


class taskall:

    def __init__(self,args,folder):
        self.folder = folder
        self.arg = args
        self.job_list = []
        # self.arg = {
        #     "BRANCH_ONE": BRANCH_ONE,
        #     "BRANCH_SIX": BRANCH_SIX,
        #     "IP": IP,
        #     "PLATFORM": PLATFORM,
        #     "ComposerSwitch": ComposerSwitch,
        #     "Version": Version
        # }
    def get_jobs(self,fordot):

        def ta(task, l1):
            if task["_class"] == "com.cloudbees.hudson.plugins.folder.Folder":
                l2 = l1 + "/" + task["name"]
                for a in task["jobs"]:
                    ta(a, l2)
            else:
                task_name = task["name"]
                jobs_name = f"{l1}/{task_name}"
                self.job_list.append(jobs_name)

        # 获取jenkins job
        jobs = server.get_jobs()

        l1 = fordot
        for job in jobs:
            if job["name"] == fordot:
                for i in job["jobs"]:
                    ta(i, l1)
        return self.job_list

    def task_build(self,task):
        try:
            old_last_build_number = server.get_job_info(task)['lastBuild']['number']
        except TypeError as e:
            old_last_build_number = 0
            print(e)

        #
        server.build_job(name=task, parameters=self.arg)
        try:
            last_build_number = server.get_job_info(task)['lastBuild']['number']
        except TypeError as ee:
            last_build_number = 0
            print(ee)

        while old_last_build_number == last_build_number:
            print("任务未添加队列开始等待")
            time.sleep(12)
            last_build_number = server.get_job_info(task)['lastBuild']['number']

        while True:

            result = server.get_build_console_output(name=task, number=last_build_number)
            # if not re.match('Finished: SUCCESS',result) or not re.match("Finished: FAILURE",result):
            if re.search('Finished: SUCCESS', result):
                message = {"task": task,"status": "SUCCESS","bulid_num": last_build_number}
                return message
            elif re.search('Finished: ', result):
                message = {"task": task, "status": "SUCCESS","bulid_num": last_build_number}
                return  message
            time.sleep(10)


    def run(self):
        tasks = self.get_jobs(self.folder)
        for task in tasks:
            try:
                print(f"构建job{task}")
                result = self.task_build(task)
                print(result)
                print(f"构建完成job{task}")
            except Exception as e:
                print(f"{task} 构建失败： {e}")
                continue

# test = taskall(folder="gh")
# a = '{"mart": "origin/master","USERNAME": "anxu","PASSWD": "Abc...123","IP": "192.168.0.102"}'

# b = json.loads(a)
# print(type(b))
# # test.run(b)


if __name__ == "__main__":
    # print(sys.argv[0:])
    if len(sys.argv)  <=3:
        print("""请输入构建参数,例如：\n
             {
                "BRANCH_ONE": BRANCH_ONE,
                "BRANCH_SIX": BRANCH_SIX,
                "IP": IP,
                "PLATFORM": PLATFORM,
                "ComposerSwitch": ComposerSwitch,
                "Version": Version
            }\n
            请输入要发布的目录: 例如 smarket_demo
        """)
    arg =  json.loads(sys.argv[1])
    fold = sys.argv[2]
    test = taskall(args=arg,folder=fold)
    print("开始执行")
    test.run()

    # self.arg = {
    #     "BRANCH_ONE": BRANCH_ONE,
    #     "BRANCH_SIX": BRANCH_SIX,
    #     "IP": IP,
    #     "PLATFORM": PLATFORM,
    #     "ComposerSwitch": ComposerSwitch,
    #     "Version": Version
    # }
    # mart = , USERNAME = "anxu", PASSWD = "Abc...123", IP = "192.168.0.102", folder = "gh"
    # data = {"mart": "origin/master","USERNAME": "anxu","PASSWD": "Abc...123","IP": "192.168.0.102"}
