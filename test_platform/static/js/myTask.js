//获取指定task_id的任务信息
var TaskInit = function (task_id) {

    function getTaskInfo(){
        // 获取某任务信息
        $.post("/interface/get_task_info/", {"taskId":task_id}, function (resp) {
            if(resp.success === "true"){
                let result = resp.data;
                document.getElementById("taskName").value=result.task_name;
                document.getElementById("taskDescribe").value=result.task_describe;
                let cases = result.task_cases;
                CaseListInit(cases);
            }else{
                window.alert("用例ID不存在")
            }
            //$("#result").html(resp);
        });
    }
    // getTaskInfo
    getTaskInfo();
};