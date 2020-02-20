
//获取指定case_id的用例信息
var CaseInit = function (case_id) {

    function getCaseInfo(){
        // 获取某个用例信息
        $.post("/interface/get_case_info/", {"caseId":case_id}, function (resp) {
            if(resp.success === "true"){
                let result = resp.data;
                document.getElementById("req_name").value=result.name;
                document.getElementById("req_url").value=result.url;
                document.getElementById("req_header").value=result.req_header;
                document.getElementById("req_parameter").value=result.req_parameter;
                document.getElementById("assert_text").value = result.responses_assert;
                if (result.req_method === "post"){
                    document.getElementById('post').setAttribute("checked","")
                }
                if (result.req_method === "json"){
                    document.getElementById('json').setAttribute("checked","")
                }
                //初始化菜单
                ProjectInit('project_name','module_name', result.project_name, result.module_name)
            }else{
                window.alert("用例ID不存在")
            }
            //$("#result").html(resp);
        });
    }
    // getCaseInfo调用
    getCaseInfo();
    
};

// 数据格式
// var dataList = [{
//     name: '项目AAAA',
//     moduleList: [
//         "模块a", "模块b", "模块c"
//     ]
// },
// {
//     name: '项目BBB',
//     moduleList: [
//         "模块1", "模块2", "模块3"
//     ]
// }
// ]