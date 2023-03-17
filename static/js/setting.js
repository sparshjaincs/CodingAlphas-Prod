function enablearea(disable, enable,flag = false){
    var dis = document.getElementById(disable);
    var ena = document.getElementById(enable);
   if(flag == false){
    dis.style.display = 'none';
    ena.style.display = 'block';
   }
   else{
    dis.style.display = 'block';
    ena.style.display = 'none';
   }
}



function savechangesform(method,user,classfield,id,field,spinner){
    document.getElementById(spinner).style.display = 'inline-block';
    if(method == 'profileimage'){
        var fd = new FormData();
        var files = document.getElementById(user).files;
        
            fd.append('file',files[0]);
            fd.append('method',method);

       
    }else{
    var value = document.getElementById(user).value;
    var i;
    var arr = document.getElementsByClassName(classfield);
    }
    if(method == 'profileimage' ){
        $.ajax({
            type:"POST",
            url:"/profile/settings/data/save/",
            data: fd,
              contentType: false,
              processData: false,
              success:function(data){
                var notify = new Notyf();
                data = JSON.parse(data);
                if(data[0] == 1){
                    notify.success("Changes saved successfully!");
                    enable_pallete(false);
                }
                else{
                    notify.error("Something might be wrong!");
                }
                document.getElementById(spinner).style.display = 'none';
              },
        });
    }else{
    $.ajax({
        type:"POST",
        url:"/profile/settings/data/save/",
        data:{
            "method":method,
            "value":value,
        },
        success:function(data){
            data = JSON.parse(data);
            var notify = new Notyf();
            if(data[0] == 1){
                for(i=0; i<arr.length ; i++){
                    arr[i].innerHTML = value;
                }
                enablearea(id,field,true);
                notify.success("Changes saved successfully!");

            }
            else{
                if(data[2] != ""){
                    notify.error(data[2]);
                }
                else{
                notify.error("Something might be wrong!");
                }
            }
            document.getElementById(spinner).style.display = 'none';
        },
    });
}

}




 
  