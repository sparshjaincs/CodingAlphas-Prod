
$(document).ready(function (e) {
    $('#VideoUploadForm').on('submit',(function(e) {
        document.getElementById('video_loader_spinner').style.display="block";
        
        e.preventDefault();
        document.getElementById('loader').style.display = 'block';
        document.getElementById('loader_bar').style.display = 'block';
        $.ajax({
            type:'POST',
            url: '/video/upload/list/',
            data:new FormData($('#VideoUploadForm')[0]),
            processData: false,
    contentType: false,
            success:function(data){
                document.getElementById("video_loader").innerHTML = "<span class='badge badge-sm badge-success'>Posted Successfully!!</span>";
                $('#Video').modal('hide');
                data = JSON.parse(data);
                if(data[0] == 'Success'){

                    var notfy = new Notyf();
                    
                    notfy.success("You uploaded post successfully!")
                    $("#myItems").prepend(`
                    <div class="card carding content mt-3 shadow-sm">
    <div class="card-header border-0">
        <div class="d-flex justify-content-between">
            <div class="d-flex justify-content-start  align-items-center">
                <div>
                        <img src="`+data[1]['photo']+`" class="rounded-circle" style="width:40px; height:40px;">
                </div>
                <div class="ml-2">
                    <div class="text-color" style="font-size: 14px; font-weight: 500; ">
                       <a href="/profile/`+data[1]['user']+`/" style="font-weight: 600;"> `+data[1]['name']+`</a> shared a video
                    </div>
                    <div class="text-color" style="font-size: 12px; font-weight: 500;">
                        `+data[1]['time']+`
                    </div>

                   
                </div>
            </div>
            <div class="d-flex justify-content-end">

            
                <div>
                    <a class=" mt-1 ml-1 btn btn-sm d-flex justify-content-center align-items-center rounded-circle" style="width:20px;height:20px;" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="fa fa-ellipsis-v"></i></a>
                <div class="dropdown-menu dropdown-menu-right" style="font-size: 12px;" aria-labelledby="dropdownMenuLink">
                    {% if request.user == i.video.user %}
                    <a class="dropdown-item" href="#"><i class="fa fa-share-alt" style="color: #E57851;"></i> Share</a>
                     {% endif %}
                    <a class="dropdown-item" href="#"><i class="fa fa-exclamation-triangle" style="color: #E57851;"></i> Report</a>
                    <a class="dropdown-item" href="#"><i class="fa fa-bookmark-o fa2" style="color: #E57851;"></i> Bookmark</a>
                   
                  </div>
                </div>
            </div>
        </div>
    </div>
    <div class="card-body ">
       


        <div>
            <video style="width:100%; max-height: 300px;"  controls muted="muted">
                <source src="`+data[1]['video']+`" >
                
              </video>
        </div>
        <div class="">
            <div class="" style="display: flex; justify-content: start; flex-wrap: wrap;">
                <a href="#" class="">
                    <div class=" mr-3" style="font-size: 20px;">
                        <i class="fa fa-heart fa2"></i> 
                    </div>
                </a>
                <a href="#" class="">
                    <div class=" mr-3" style="font-size: 20px;">
                        <i class="fa fa-comment fa2"></i> 
                    </div>
                </a>
                <a href="#" class="">
                    <div class=" mr-3" style="font-size: 20px;">
                        <i class="fa fa-paper-plane fa2"></i> 
                    </div>
                </a>
                <a href="#" class="">
                    <div class=" mr-2" style="font-size: 20px;">
                        <i class="fa fa-bookmark fa2"></i> 
                    </div>
                </a>
            
            
                
              
            
            
                
            </div>
            
       
        </div> 
        <div class="mt-1">
            <a  style="font-weight: 600; font-size: 14px;">
                Liked by 0 users.
              </a>
        </div>
           <div class="">
               <div style="font-size: 14px;" class="text-color hide-me">
                <div>
                    <span id="less{{i.id}}">
                    <a href="/profile/`+data[1]['user']+`" style="font-weight: 600;">
                        `+data[1]['user']+`  :
                      </a> `+data[1]['desc'].substring(0,140)+`
                      <a onclick="expandable('{{i.id}}')" style="cursor: pointer;">read more</a>
                    </span>

                      <span id="more{{i.id}}" style="display: none;">
                        <div style="font-size: 14px;" class="text-color mt-2">
                            <a href="/profile/`+data[1]['user']+`" style="font-weight: 600;">
                                `+data[1]['user']+`  :
                              </a> 
                            `+data[1]['desc']+`
                           
                        </div>
                    
                        <div class="d-flex flex-wrap" id="tag"> 
                           
                           
                           </div>
                      </span>
                </div>
            
               </div>

          
           </div>
            
            <div>
               <div>
                <a class="" data-toggle="collapse" href="#collapseExample{{i.id}}"  role="button" aria-expanded="false" aria-controls="collapseExample{{i.id}}" >
                    <div class="" style="font-size: 13px; font-weight:500">
                        View all 12 comments
                    </div>
                </a>
               </div>

                <div class="collapse mt-3 " id="collapseExample{{i.id}}">
                    <div class="card card-body border-0" style="font-size: 12px;">
                       <div class=" d-flex justify-content-center">
                        <i class="fa fa-spinner fa-spin" style="color: #E57851;"></i>
                       </div>
                       </div>
                  </div>
            </div>

    </div>

    <div class="card-footer border-0">
        <form>
            <div class="d-flex justify-content-between">
        <div style="width:100%;" class="d-flex justify-content-start align-items-center">
         <span class="mr-2">  <i class="fa fa-comment" style="color: #BCC0C4;"></i> </span>  <input type="text" required style="width:100%; background:none; border:none; font-size:13px;" placeholder="Add a public comment">
        </div>
        <div>
            <button type="submit" class="btn btn-sm" style="background: none; color: #2EA8E6;">
                Post
            </button>   

        </div>
    </div>
    </form>
    </div>
</div>
                    `);
                    var s = "";
                    var tags = data[1]['tags'].split(",");
                    var i=0;
                    for(i=0; i<tags.length; i++){
                        s+=`  <a href="/tags/`+tags[i]+`" style="font-size: 12px;" class="btn btn-sm tag m-1">`+tags[i]+`</a>`;
                    }
                    document.getElementById("tag").innerHTML = s;
                }

                else{
                    var notfy = new Notyf();
                    notfy.warning("Some eror occurred!")
                }
                document.getElementById('loader').style.display = 'none';
                document.getElementById('loader_bar').style.display = 'none';
                
            },
            error: function(data){
                console.log("error");
                console.log(data);
            }
        });
    }));

  
});