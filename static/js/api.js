var lecturerLogin = document.getElementById('lecturer-login-form');
var studentLogin = document.getElementById('student-login-form');
var createAttendance = document.getElementById('create-attendace-form');
var takeAttendance = document.getElementById('take-attendace-form');
var deleteAttendance = document.querySelectorAll("#delete-attendace");
var alertMsg = document.querySelector('#alert');
var alertCPMsg = document.querySelector('#alert_change_psw');
var alertDeleteMsg = document.querySelector('#alertDelete');
var alertMsgAvatar = document.querySelector('#avatar-alert');
var alertText = document.querySelector('#alert p');
var alertDash = document.querySelector('#alertDash');
var alertDashText = document.querySelector('#alertDash p');
var logout = document.getElementById('logout-btn');
var lecturerRegister = document.getElementById('lecturer-register-form');
var studentRegister = document.getElementById('student-register-form');
var lecturerProfileUpdate = document.getElementById('lecturer-profile-update');
var studentProfileUpdate = document.getElementById('student-profile-update');
var changePasswordUpdate = document.getElementById('change-password-update');
var uploadAvatar = document.getElementById('avatar-upload-form');
var passswordReset = document.getElementById('password-rest-form');
var passswordConfirm = document.getElementById('password-rest-confirm');
var spinner = document.getElementById('ajax-loader');
var feedback = document.getElementById('feedback-form');
var span = document.getElementById('span');
var tableRowRemove = document.querySelectorAll('#tableRowRemove');
var togglePassword = document.querySelector('#togglePassword');


function alertMessage(bg,msg,selector) {
    selector.innerHTML += `<div class="alert ${bg} text-white alert-dismissible fade show" role="alert">
                                <div class="d-flex justify-content-between">
                                    <p class="p-1">${msg}</p>
                                    <button type="button" class="close m-2" data-dismiss="alert" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>	
                                    </div>											
                            </div>`
}

//TogglePassword
function myFunctionToggle() {
    var password = document.querySelector('#password');
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    togglePassword.classList.toggle('fa-eye-slash');
}

// Toggled Changed Password
function changePasswordToggled(psd, toggled_id) {
    var password = document.querySelector("#"+psd);
    var togglePsd = document.querySelector("#"+toggled_id);
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    togglePsd.classList.toggle('fa-eye-slash');
}

//TitleCase
String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};

var getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

var csrftoken = getCookie('csrftoken');

//Lecturer Register Form
if (lecturerRegister) {
    lecturerRegister.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('lecturer-register-form');
        let email = document.getElementById('email');
        let password = document.getElementById('password');
        let first_name = document.getElementById('first_name');
        let gender = document.getElementById('gender');
        let contact = document.getElementById('contact');
        let department = document.getElementById('department');
        let faculty = document.getElementById('faculty');

        var newData =   {
            "email": email.value,
            "password": password.value,
            "first_name": first_name.value.split(" ")[0].toProperCase(),
            "last_name": first_name.value.split(" ").pop().toProperCase(),
            "gender": gender.value,
            "contact": contact.value,
            "is_student": false,
            "is_lecturer": true,
            "signup_confirmation": false,
            "lecturer": {
                "department": department.value,
                "faculty": faculty.value
            }
        };

        var dataJson = JSON.stringify(newData);
        console.log(dataJson);

        $.ajax({
            type: "POST",
            beforeSend: function() {
                spinner.style.visibility = 'visible';
            },        
            url: "/user/api/register/lecturer/",        
            data: dataJson,  
            success: function(result) {
                console.log(result);
                document.title = "Registered Lecturer";
                alertMessage("bg-success",`${result["message"]}`,alertMsg)
                form.reset();
            },
            error: function (error) {
                console.log(error);                
                if (error["status"] === 400) {
                   if (error["responseJSON"]["email"][0]) {
                        alertMessage("bg-danger",`This user ${email.value} already exist.`,alertMsg);
                    } 
                }
                if (error["status"] === 500) {
                    alertMessage("bg-danger","Internal Server Error!",alertMsg);
                }                
            },
            complete: function(){
                spinner.style.visibility = 'hidden';
            },
            dataType: "json",
            contentType: "application/json"
        });
    });
};

//Student Register Form
if (studentRegister) {
    studentRegister.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('student-register-form');
        let email = document.getElementById('email');
        let password = document.getElementById('password');
        let password2 = document.getElementById('compsd');
        let first_name = document.getElementById('first_name');
        let gender = document.getElementById('gender');
        let contact = document.getElementById('contact');
        let dob = document.getElementById('dob');
        let level = document.getElementById('level');
        let semester = document.getElementById('semester');
        let matric_no = document.getElementById('matric_no');
        let department = document.getElementById('department');

        var newData =   {
            "email": email.value,
            "password": password.value,
            "first_name": first_name.value.split(" ")[0].toProperCase(),
            "last_name": first_name.value.split(" ").pop().toProperCase(),
            "gender": gender.value,
            "contact": contact.value,
            "is_student": true,
            "is_lecturer": false,
            "signup_confirmation": false,
            "student": {
                'matric_no': matric_no.value.toUpperCase(), 
                'semester': semester.value, 
                'level': level.value, 
                'dob': dob.value, 
                'department': department.value
            }
        };

        var dataJson = JSON.stringify(newData);
        console.log(dataJson);
        if (/^(sci|fas)(\w+)$/i.test(matric_no.value) === false || matric_no.value.length != 11) {
            alertMessage("bg-danger","Invalid Matriculation Number",alertMsg);
            matric_no.value = '';
        } else if (password.value != password2.value) {
            alertMessage("bg-danger","Password does not match!",alertMsg);
        } else if (password.value.length < 8) {
            alertMessage("bg-danger","Password must not be less than 8 characters",alertMsg);
        }
        else {
            $.ajax({
                type: "POST",
                beforeSend: function() {
                    spinner.style.visibility = 'visible';
                },        
                url: "/user/api/register/student/",        
                data: dataJson,  
                success: function(result) {
                    console.log(result);
                    document.title = "Registered Student";
                    alertMessage("bg-success",`${result["message"]}`,alertMsg)
                    form.reset();
                },
                error: function (xhr, status, error) {
                    err = xhr.responseText.split("\"")[3].replace(/"|'/g,);
                    if (xhr["status"] === 400) {
                        alertMessage("bg-danger",`${err}`,alertMsg);
                    }                    
                    if (xhr["status"] === 500) {
                        alertMessage("bg-danger","Internal Server Error!",alertMsg);
                    }
                },
                complete: function(){
                    spinner.style.visibility = 'hidden';
                },
                dataType: "json",
                contentType: "application/json"
            });  
        }        
    });
};

// Upload User Avatar
if (uploadAvatar) {
    uploadAvatar.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('avatar-upload-form');
        let imageTag = document.getElementsByTagName('IMG');
        let input = document.getElementById('id_avatar');
        let data_img = new FormData();
        data_img.append('avatar', input.files[0], input.files[0].name);

        if ( /\.(jpe?g|png|gif)$/i.test(input.files[0].name) === false) { 
            //Validating the Image Type
            alertMessage('bg-danger','image must be jpg/png/gif!',alertMsgAvatar); 
        } else if (input.files[0].size > 1048576) {
            alertMessage('bg-danger','Image file larger than 1MB!',alertMsgAvatar);
        } else {
            $.ajax({
                type: "POST",
                beforeSend: function() {
                    spinner.style.visibility = 'visible';
                },   
                url: "/user/api/upload_avatar/",
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                contentType: false,
                processData: false,
                data: data_img,
                success: function(result) {
                    console.log("result *************", result['avatar']);
                    imageTag.src = result['avatar'];
                    document.title = "Avatar Uploaded";              
                    alertMessage('bg-success','Avatar Uploaded Successfully!',alertMsgAvatar);
                    // console.log(input.files[0].size);
                },
                error: function (error) {
                    console.log(error);
                    console.log(error["responseJSON"]["detail"]);
                    alertMessage('bg-danger','Avatar not uploaded!',alertMsgAvatar);
                    if (error.status === 500) alertMessage('bg-danger','Server Error!',alertMsgAvatar);
                },
                complete: function(){
                    spinner.style.visibility = 'hidden';
                },
            });            
        }
        form.reset();        
    });   
}

//Lecturer Login Form
if (lecturerLogin) {
    lecturerLogin.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('lecturer-login-form');
        let email = document.getElementById('email');
        let password = document.getElementById('password');
            
        var newData = {
            "email": email.value,
            "password": password.value
        };

        var dataJson = JSON.stringify(newData);
        console.log(dataJson);

        $.ajax({
            type: "POST",
            beforeSend: function() {
                spinner.style.visibility = 'visible';
            },        
            url: "/user/api/login/lecturer/",
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: dataJson,
            success: function(result) {
                console.log(result);
                console.log(result.token);
                document.querySelector('title').textContent = "Lecturer|Login";
                if (result['success'] == "True") {
                    window.location.href = `${window.location.origin}/create/attendance/`;
                    // alert("User Login succefully!");                        
                } else {
                    window.location.href
                }                
                form.reset();
            },
            error: function (error) {
                if (error['status'] === 500) {
                    alertMessage("bg-danger",`${error["statusText"]}`,alertMsg)
                }
                console.log(error); 
                console.log(error["responseJSON"]["non_field_errors"][0]);
                alertMessage("bg-danger",`${error["responseJSON"]["non_field_errors"][0]}`,alertMsg);                                     
            },
            complete: function(){
                spinner.style.visibility = 'hidden';
            },
            dataType: "json",
            contentType: "application/json"
        });
    });
}

//Student Login Form
if (studentLogin) {
    studentLogin.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('student-login-form');
        let email = document.getElementById('email');
        let password = document.getElementById('password');
            
        var newData = {
            "email": email.value,
            "password": password.value
        };

        var dataJson = JSON.stringify(newData);
        console.log(dataJson);

        $.ajax({
            type: "POST",
            beforeSend: function() {
                spinner.style.visibility = 'visible';
            },        
            url: "http://127.0.0.1:8000/user/api/login/student/",
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: dataJson,
            success: function(result) {
                console.log(result);
                if (result['success'] == "True") {
                    window.location.href = `${window.location.origin}/take/attendance/`;
                    // alert("User Login succefully!");                        
                } else {
                    window.location.href
                }                
                form.reset();
            },
            error: function (error) {
                if (error['status'] === 500) {
                    alertMessage("bg-danger",`${error["statusText"]}`,alertMsg)
                }
                console.log(error); 
                console.log(error["responseJSON"]["non_field_errors"][0]);
                alertMessage("bg-danger",`${error["responseJSON"]["non_field_errors"][0]}`,alertMsg); 
                spinner.style.visibility = 'hidden';                                    
            },
            complete: function(){
                spinner.style.visibility = 'hidden';
            },
            dataType: "json",
            contentType: "application/json"
        });
    });
}

//Logout User from the SideBar
if (logout) {            
	logout.addEventListener('click', function(event) {
        $.ajax({
            type: "POST",
            beforeSend: function() {
                spinner.style.visibility = 'visible';
            },   
            url: "/user/api/logout/",
            headers: {
                'X-CSRFToken': csrftoken,
            },
            success: function(result) {
                console.log(result);
                redirect_path = `${window.location.origin}`
                window.location.href = redirect_path
            },
            error: function (error) {
                console.log(error);
                console.log(error["responseText"]);
                console.log(error["responseJSON"]["detail"]);
            },
            complete: function(){
                spinner.style.visibility = 'hidden';
            },
            dataType: "json",
            contentType: "application/json"
        });
	});
}

//Logout User from the NavBar
function logoutNow() {
    $.ajax({
        type: "POST",
        beforeSend: function() {
            spinner.style.visibility = 'visible';
        },   
        url: "/user/api/logout/",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(result) {
            console.log(result);
            redirect_path = `${window.location.origin}`
            window.location.href = redirect_path
        },
        error: function (error) {
            console.log(error);
            console.log(error["responseText"]);
            console.log(error["responseJSON"]["detail"]);
        },
        complete: function(){
            spinner.style.visibility = 'hidden';
        },
        dataType: "json",
        contentType: "application/json"
    });
}

//Sent Password Reset Link
if (passswordReset) {
    passswordReset.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('password-rest-form');
        let email = document.getElementById('email');
            
        var newData = {
            "email": email.value,
        };

        var dataJson = JSON.stringify(newData);
        console.log(dataJson);
        $.ajax({
            type: "POST",
            beforeSend: function() {
                spinner.style.visibility = 'visible';
            },     
            url: "/api/password_reset/",
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: dataJson,            
            success: function(result) {
                console.log(result);
                alertMessage("bg-success","Please check your email for reset link!",alertMsg)
            },
            error: function (error) {
                console.log(error);
                alertMessage("bg-danger","Sorry! Link not sent!",alertMsg)
            },
            complete: function(){
                spinner.style.visibility = 'hidden';
            },
            dataType: "json",
            contentType: "application/json"
        });
        form.reset();
	});
}

//Reset Password
if (passswordConfirm) {
    passswordConfirm.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('password-rest-confirm');
        let password = document.getElementById('password');
        let con_password = document.getElementById('con_password');
        let token = document.getElementById('token');
            
        var newData = {
            "password": password.value,
            "token": token.value
        };

        var dataJson = JSON.stringify(newData);
        console.log(dataJson);
        if (password.value != con_password.value) {
            alertMessage("bg-danger","Password does not match!",alertMsg)
        } else {
            $.ajax({
                type: "POST", 
                beforeSend: function() {
                    spinner.style.visibility = 'visible';
                },   
                url: "/api/password_reset/confirm/",
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                data: dataJson,
                success: function(result) {
                    console.log(result);
                    alertMessage("bg-success","Password reset successfully!",alertMsg)
                },
                error: function (error) {
                    console.log(error);
                    if (error["responseJSON"]["password"][0]) {
                        alertMessage("bg-danger",`${error["responseJSON"]["password"][0]}`,alertMsg); 
                    } else {
                       alertMessage("bg-danger","Password reset unsuccessfully!",alertMsg) 
                    }                    
                },
                complete: function(){
                    spinner.style.visibility = 'hidden';
                },
                dataType: "json",
                contentType: "application/json"
            });    
        }        
        form.reset();
	});
}

//Lecturer Update Profile
if (lecturerProfileUpdate) {
    lecturerProfileUpdate.addEventListener('submit', function(event) {
        event.preventDefault();
        let first_name = document.getElementById('first_name');
        let last_name = document.getElementById('last_name')
        let gender = document.getElementById('gender');
        let contact = document.getElementById('contact'); 
        let department = document.getElementById('department'); 
        let faculty = document.getElementById('faculty');
        var text_department = department.options[department.selectedIndex].text;
        var text_faculty = faculty.options[faculty.selectedIndex].text;
        var newData = {
            "first_name": first_name.value.toProperCase(),
            "last_name": last_name.value.toProperCase(),
            "gender": gender.value,
            "contact": contact.value,
            "lecturer": {
                "department": text_department,
                "faculty": text_faculty
            }
        };
        var dataJson = JSON.stringify(newData);
        console.log(dataJson)
        $.ajax({
            type: "PUT",
            beforeSend: function() {
                spinner.style.visibility = 'visible';
            },  
            url: "/user/api/lecturer_update_profile/",
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: dataJson,
            success: function(result) {
                // alert("Profile Updated Updated Successfully!")
                alertMessage("bg-success","Profile Updated Successfully!",alertMsg);
            },
            error: function (error) {
                console.log(error);
                if (error["responseJSON"]["old_password"][0]) {
                    alertMessage("bg-danger",`${error["responseJSON"]["old_password"][0]}`,alertMsg); 
                }
            },
            complete: function(){
                spinner.style.visibility = 'hidden';
            },
            dataType: "json",
            contentType: "application/json"
        });
    });   
}

//Student Update Profile
if (studentProfileUpdate) {
    studentProfileUpdate.addEventListener('submit', function(event) {
        event.preventDefault();           
        let first_name = document.getElementById('first_name');
        let last_name = document.getElementById('last_name')
        let gender = document.getElementById('gender');
        let contact = document.getElementById('contact');
        let dob = document.getElementById('dob');
        let level = document.getElementById('level');
        let semester = document.getElementById('semester');      
        var text_semester = semester.options[semester.selectedIndex].text;
        var text_level = level.options[level.selectedIndex].text;

        var newData =   {
            "first_name": first_name.value.toProperCase(),
            "last_name": last_name.value.toProperCase(),
            "gender": gender.value,
            "contact": contact.value,
            "student": {
                'semester': text_semester, 
                'level': text_level, 
                'dob': dob.value,
            }
        };

        var dataJson = JSON.stringify(newData);
        console.log(dataJson)
        $.ajax({
            type: "PUT",
            beforeSend: function() {
                spinner.style.visibility = 'visible';
            },    
            url: "/user/api/student_update_profile/",
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: dataJson,
            success: function(result) {
                // alert("Profile Updated Updated Successfully!")
                alertMessage("bg-success","Profile Updated Successfully!",alertMsg);
            },
            error: function (error) {
                console.log(error);
                if (error["responseJSON"]["old_password"][0]) {
                    alertMessage("bg-danger",`${error["responseJSON"]["old_password"][0]}`,alertMsg); 
                }
            },
            complete: function(){
                spinner.style.visibility = 'hidden';
            },
            dataType: "json",
            contentType: "application/json"
        });
    });   
}

// Change Password
if (changePasswordUpdate) {
    changePasswordUpdate.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('change-password-update');
        let old_password = document.getElementById('old_password');
        let new_password = document.getElementById('new_password');
        let confirm_password = document.getElementById('confirm_password');            
        var newData = {
            "old_password": old_password.value,
            "password": new_password.value,
            "password2": confirm_password.value        
        };
        var dataJson = JSON.stringify(newData);

        if (new_password.value !== confirm_password.value) {
            alertMessage("bg-danger","Password fields didn't match.",alertCPMsg);
        } else {
            $.ajax({
                type: "PUT",
                beforeSend: function() {
                    spinner.style.visibility = 'visible';
                },     
                url: "/user/api/change_password/",
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                data: dataJson,
                success: function(result) {
                    // alert("Password Updated Successfully!")
                    alertMessage("bg-success","Password Updated Successfully!",alertCPMsg);
                    form.reset()
                    
                },
                error: function (error) {
                    console.log(error);
                    console.log(error["responseText"]);
                    if (error["responseJSON"]["old_password"][0]) {
                        alertMessage("bg-danger",`${error["responseJSON"]["old_password"][0]}`,alertCPMsg);
                    }
                    form.reset()
                },
                complete: function(){
                    spinner.style.visibility = 'hidden';
                },
                dataType: "json",
                contentType: "application/json"
            });    
        }
    });   
}

// Create Attendance
if (createAttendance) {
    createAttendance.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('create-attendace-form');
        let title = document.getElementById('title');
        let level = document.getElementById('level');
        let department = document.getElementById('department');
        let course = document.getElementById('course');
        let duration = document.getElementById('duration');            

        var newData = {
            "title": title.value,
            "level": level.value,
            "department": department.value,
            "course": course.value.toUpperCase(), 
            "duration": duration.value      
        };
        var dataJson = JSON.stringify(newData);
        console.log(dataJson);
        $.ajax({
            type: "POST",
            beforeSend: function() {
                spinner.style.visibility = 'visible';
            },   
            url: "/api/create_attendance/",
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: dataJson,
            success: function(result) {
                console.log(result);
                alertMessage("bg-success",`${result['message']}`,alertMsg);
                setTimeout(function background() {
                    span.classList.add("badge bg-warning");                    
                }, 2000);
            },
            error: function (error) {
                console.log(error);
                // console.log(error["responseJSON"]["detail"]);
                if (error['status'] === 500) alertMessage("bg-danger","Internal Server Error",alertMsg);
                if (error['status'] === 400) alertMessage("bg-danger",`${error["responseJSON"]["non_field_errors"][0]}`,alertMsg);
            },
            complete: function(){
                spinner.style.visibility = 'hidden';
            },
            dataType: "json",
            contentType: "application/json"
        });
        form.reset();
    })
}

// Take Attendance
if (takeAttendance) {
    takeAttendance.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('take-attendace-form');
        let code = document.getElementById('code');            
        var newData = {
            "code": code.value,       
        };
        var dataJson = JSON.stringify(newData);
        console.log(dataJson);
        $.ajax({
            type: "POST",
            beforeSend: function() {
                spinner.style.visibility = 'visible';
            },   
            url: "/api/take_attendance/",
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: dataJson,
            success: function(result) {
                console.log(result);
                alertMessage("bg-success",`${result['message']}`,alertMsg);
            },
            error: function (error) {
                console.log(error);
                if (error['status'] === 400) {
                    if (error["responseJSON"][0]) {
                        alertMessage("bg-danger",`${error["responseJSON"][0]}`,alertMsg);                    
                    }     
                }
                if (error['status'] === 500) alertMessage("bg-danger","Internal Server Error",alertMsg);               
            },
            complete: function(){
                spinner.style.visibility = 'hidden';
            },
            dataType: "json",
            contentType: "application/json"
        });
        form.reset();
    })
}

// Delete Attendance
function deleteCreatedAttendance(pk) {
    $.ajax({
        type: "DELETE",
        beforeSend: function() {
            spinner.style.visibility = 'visible';
        },   
        url: `/api/delete_attendance/${pk}/`,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(result) {
            console.log(result);
            alertMessage("bg-success","Attendance Deleted Successfully",alertDeleteMsg);
        },
        error: function (error) {
            console.log(error);
            if (error['status'] === 400) alertMessage("bg-danger",`${error["responseJSON"]["non_field_errors"][0]}`,alertDeleteMsg);
            if (error['status'] === 500) alertMessage("bg-danger","Internal Server Error",alertMsg);
        },
        complete: function(){
            spinner.style.visibility = 'hidden';
        },
        dataType: "json",
        contentType: "application/json"
     });
}

function removeCreatedAttendance(id) {     
    if (id) {
        console.log(id);
        idk = parseInt(id);
        tableRowRemove[id].style.display = "None";
        deleteCreatedAttendance(id);                  
    }
}

//Feedback
if (feedback) {
    feedback.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('feedback-form');
        let subject = document.getElementById('subject');
        let message = document.getElementById('message');           
        var newData = {
            "subject": subject.value.toProperCase(),
            "message": message.value
        };
        var dataJson = JSON.stringify(newData);
        console.log(dataJson);
        $.ajax({
            type: "POST",
            beforeSend: function() {
                spinner.style.visibility = 'visible';
            },   
            url: "/api/feedback/",
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: dataJson,
            success: function(result) {
                console.log(result);
                alertMessage("bg-success","Feedback submitted successfully!",alertMsg);
            },
            error: function (error) {
                console.log(error);
                // console.log(error["responseText"]);
                // console.log(error["responseJSON"]["detail"]);
                if (error['status'] === 400) alertMessage("bg-danger",`${error["responseJSON"]["non_field_errors"][0]}`,alertMsg);
                if (error['status'] === 500) alertMessage("bg-danger","Internal Server Error",alertMsg);
            },
            complete: function(){
                spinner.style.visibility = 'hidden';
            },
            dataType: "json",
            contentType: "application/json"
        });
        form.reset();
    });    
}
