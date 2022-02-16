schedule_frame = document.getElementById("add-job-form");
view_jobs_frame = document.getElementById("view-jobs-frame");

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

show_schedule_frame = () =>{
    schedule_frame.style.display = "block";
    view_jobs_frame.style.display="none";
}

show_view_jobs_frame = () =>{
    schedule_frame.style.display = "none";
    view_jobs_frame.style.display="block";
    // show_loader(0);
    // make api call
}
