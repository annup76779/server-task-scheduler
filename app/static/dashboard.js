schedule_frame = document.getElementById("add-job-form");
view_jobs_frame = document.getElementById("view-jobs-frame");
table = document.querySelector("#table tbody");
date_input_box = document.querySelector("#sdate");
var load_more = true;
var current_page_count = 1;
var mini_loader = document.querySelector("#loader");
current_url = "/api/get_all_jobs";

show_user_option = (el) =>{
    let target = document.getElementById('user_options');
    if (el.getAttribute('data-toggle') === "off"){
        target.style.display = "block";
        el.setAttribute('data-toggle',"on");
    }
    else{
        target.style.display = "none";
        el.setAttribute('data-toggle',"off");
    }
}

requestDate = () =>{
    date = date_input_box.value;
    current_url = `/api/get_job_by_date?scheduledFor=${date}&page=${current_page_count}`;
    table.innerHTML = "";
    // current_page_count = 1;
    load_more = true;
    getJobs();
}

allJobs = () =>{
    current_url = `/api/get_all_jobs?page=${current_page_count}`;
    table.innerHTML = "";
    // current_page_count = 1;
    load_more = true;
    getJobs();
}

async function getJobs(){
    if (load_more){  
        if (current_page_count!=1)
            mini_loader.style.display = "block";
        let options = {
            "Accpts": "application/*",
        }
        response = await fetch(current_url,{
                method: "GET",
                headers: options
            }).then(function(response){
                if (response.status == 200)
                    return response.json();
                return Promise.reject(response);
            }).then(function(data){
                return data;
            }).catch(function(error){
                console.log(error);
            });
        if (response.status = true)
            settle_jobs(response);
        else
            alert(response.response);
        mini_loader.style.display = "none";
    }
}

function settle_jobs(response){
    for(var i = 0; i < response.jobs.length ; i++){
        job = response.jobs[i];
        html = `
        <tr>
            <th scope="row">${i+1}</th>
            <td>${job.type_}</td>
            <td>${job.ref_name}</td>
            <td>${job.date_}</td>
            <td>${job.time_}</td>
            <td>${job.tool_used}</td>
            <td>
                <a href="/api/job/${job.id}" target="_blank">View</a>
            </td>
        </tr>
        `
        table.insertAdjacentHTML("beforeend", html);
        // if (current_page_count >= response.total_pages){
        //     load_more = false; 
        //     // load_more_btn.remove();
        // }
        // else if (current_page_count < response.total_pages){
        //     current_page_count += 1;
        //     // load_more_btn.style.display ="block";
        // }
    }
    // alert(current_page_count)
}


show_schedule_frame = () =>{
    schedule_frame.style.display = "block";
    view_jobs_frame.style.display="none";
}

show_view_jobs_frame = () =>{
    schedule_frame.style.display = "none";
    view_jobs_frame.style.display="block";
    getJobs()
}
