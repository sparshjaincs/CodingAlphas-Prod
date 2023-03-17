
var ctx = document.getElementById('myChart').getContext('2d');
var gradient = ctx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, 'rgba(250,174,50,1)');   
gradient.addColorStop(1, 'rgba(250,174,50,0)');
var myChart = new Chart(ctx, {
    type: 'line',
    responsive:true,
    data: {
        labels: ['', '', '', '', '', ''],
        datasets: [{
            label: 'Views',
            data: [0, 0, 0, 0, 0, 0],
            fill: true,
            backgroundColor:gradient,
            borderColor: 'rgba(250,174,50,1)',
            tension: 0.1,
            borderWidth: 1
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: 'Custom Chart Title'
            },
            legend:{
                display:false,
            }
        },
        animation: {
            onComplete: () => {
              delayed = true;
            },
            
        },
        scales: {
            x: {
                stacked: true,
              },
              y: {
                stacked: true
              }
        }
    }
});


function fetchingcontent(id,currindex=0,updated_index=0){
    $.ajax({
        type:"GET",
        url:"/blogs/analytics/data/fetch/",
        data:{
            "id":id,
            "index":currindex,
            "update":updated_index,
        },
        success:function(dataval){
            dataval = JSON.parse(dataval);
            var i;
          
              // Would update the first dataset's value of 'March' to be 50
            for(i=0; i<=dataval['y'].length; i++){
                myChart.data.datasets[0].data[i] = dataval['y'][i]; 
                myChart.data.labels[i] = dataval['x'][i];
            }
            myChart.options.plugins.title.text = dataval['title'];
            myChart.update();
            myChart3.data.datasets[0].data[0] = dataval['stack'][0];
            myChart3.data.datasets[0].data[1] = dataval['stack'][1];
            myChart3.data.datasets[0].data[2] = dataval['stack'][2];

            myChart3.data.datasets[0].data[3] = dataval['stack'][3];
            myChart3.options.plugins.title.text = dataval['title'];
            myChart3.update();

        }
    });
}

window.onload = loaddata();
function loaddata(){
    fetchingcontent(-1);
}



var ctx1 = document.getElementById('myChart1').getContext('2d');
var gradient1 = ctx1.createLinearGradient(0, 0, 0, 400);
gradient1.addColorStop(0, 'rgba(250,174,50,1)');   
gradient1.addColorStop(1, 'rgba(250,174,50,0.1)');

var gradient2 = ctx1.createLinearGradient(0, 0, 0, 400);
gradient2.addColorStop(0, 'rgba(46, 168, 230,1)');   
gradient2.addColorStop(1, 'rgba(46, 168, 230,0.1)');

var gradient3 = ctx1.createLinearGradient(0, 0, 0, 400);
gradient3.addColorStop(0, 'rgba(177, 60, 46,1)');   
gradient3.addColorStop(1, 'rgba(177, 60, 46,0.1)');

var gradient4 = ctx1.createLinearGradient(0, 0, 0, 400);
gradient4.addColorStop(0, 'rgba(110, 190, 70,1)');   
gradient4.addColorStop(1, 'rgba(110, 190, 70,0.1)');
var myChart1 = new Chart(ctx1, {
    type: 'bar',
    responsive:true,
    data: {
        labels: ['Likes', 'Views', 'Saves', 'Comments'],
        datasets: [{
         
            data: [0, 0, 0, 0],
            fill: true,
            backgroundColor:[gradient3,gradient1,gradient2,gradient4],
            borderColor: ['rgba(177, 60, 46,1)','rgba(250,174,50,1)','rgba(46, 168, 230,1)','rgba(110, 190, 70,1)'],
            tension: 0.1,
            borderWidth: 1
        }]
    },
    options: {
        legend: {
            display: false
        },
          tooltips: {
            callbacks: {
              label: function(tooltipItem) {
            console.log(tooltipItem)
                return tooltipItem.yLabel;
            }
          }
        },
        plugins: {
            title: {
                display: true,
                text: 'Total likes, views, comments, saves of your published articles (Total Content Interaction).'
            },
            legend:{
                display:false
            }
        },
        
       
    }
});

function fetchingcontentall(currindex=0,updated_index=0){
    $.ajax({
        type:"GET",
        url:"/blogs/analytics/data/fetch/all/",
        data:{
           
            "index":currindex,
            "update":updated_index,
        },
        success:function(dataval){
            dataval = JSON.parse(dataval);
            var i;
        
              // Would update the first dataset's value of 'March' to be 50
            for(i=0; i<=3; i++){
               
                myChart1.data.datasets[0].data[i] = dataval[i];
            }
           
            myChart1.update();
            myChart5.data.datasets[0].data[0] = dataval[4];
            myChart5.data.datasets[0].data[1] = dataval[5];
            myChart5.update();
            document.getElementById('likecount') = 1;
          

        }x
    });
}

window.onload = loaddataall();
function loaddataall(){
    fetchingcontentall();
}


var ctx3 = document.getElementById('myChart3').getContext('2d');
var gradient5 = ctx3.createLinearGradient(0, 0, 0, 400);
gradient5.addColorStop(0, 'rgba(250,174,50,1)');   
gradient5.addColorStop(1, 'rgba(250,174,50,0)');

var gradient6 = ctx3.createLinearGradient(0, 0, 0, 400);
gradient6.addColorStop(0, 'rgba(46, 168, 230,1)');   
gradient6.addColorStop(1, 'rgba(46, 168, 230,0)');

var gradient7 = ctx3.createLinearGradient(0, 0, 0, 400);
gradient7.addColorStop(0, 'rgba(177, 60, 46,1)');   
gradient7.addColorStop(1, 'rgba(177, 60, 46,0)');

var gradient8 = ctx3.createLinearGradient(0, 0, 0, 400);
gradient8.addColorStop(0, 'rgba(110, 190, 70,1)');   
gradient8.addColorStop(1, 'rgba(110, 190, 70,0)');
var myChart3 = new Chart(ctx3, {
    type: 'bar',
    responsive:true,
    data: {
        labels: ['Likes', 'Views', 'Saves', 'Comments'],
        datasets: [{
          
            data: [12, 0, 0, 0],
            fill: true,
            backgroundColor:[gradient7,gradient5,gradient6,gradient8],
            borderColor: ['rgba(177, 60, 46,1)','rgba(250,174,50,1)','rgba(46, 168, 230,1)','rgba(110, 190, 70,1)'],
            tension: 0.1,
            borderWidth: 1
        }]
    },
    options:{
        plugins: {
            title: {
                display: true,
                text: 'Custom Chart Title'
            },
            legend:{
                display:false
            }
        },
    }
 
});


var ctx5 = document.getElementById('myChart5').getContext('2d');
var myChart5 = new Chart(ctx5, {
    type: 'pie',
    data: {
        labels: ['Published', 'Drafts'],
        datasets: [{
            label: '# of Votes',
            data: [, ],
            backgroundColor: [
               
           
                'rgba(110, 190, 70, 0.6)',
                'rgba(46, 168, 230, 0.6)'
            ],
            borderColor: [
               
                'rgba(110, 190, 70, 1)',
                'rgba(46, 168, 230, 1)'
            ],
            borderWidth: 1

        }]
    },
    options: {
        plugins: {
            legend: {
              display: false
            }
          },
       
       
       
    }
});
