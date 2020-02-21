
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


//获取用例信息列表
var CaseListInit = function () {

    var options = "";
    function getCaseListInfo(){
        // 获取用例信息列表
        $.get("/interface/get_case_list/", {}, function (resp) {
            if(resp.success === "true"){
               let cases = resp.data;

                for (let i =0; i < cases.length; i++){
                    let option = '<input type="checkbox" name="box" value="' + cases[i].id +'" /> '+ cases[i].name +'<br>';
                    options = options + option
                }
                let devCaseList = document.querySelector(".caseList");
                devCaseList.innerHTML = options;
            }else{
                window.alert("获取用例失败")
            }
            //$("#result").html(resp);
        });
    }
    // getCaseListInfo
    getCaseListInfo();
};
