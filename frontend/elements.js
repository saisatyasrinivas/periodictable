$(document).ready(function(){
    setTimeout(function(){
        var url = 'http://localhost:5000/periodictable/classifications/';
        var url1 = 'http://localhost:5000/periodictable/standard_states/';
        var url2 = 'http://localhost:5000/periodictable/blocks/';
        var url3 = 'http://localhost:5000/periodictable/groups/';
        var url4 = 'http://localhost:5000/periodictable/periods/';
        
        callEndPoint(url, 'classification');
        callEndPoint(url1, 'standardState');
        callEndPoint(url2, 'block');
        callEndPoint(url3, 'group');
        callEndPoint(url4, 'period');
        
    },3000)
})

function callEndPoint(url,id){
    $.ajax({
        url: url,
        type: 'GET',
        success: function(response){
            let options = response.options;
            let htmlCode = "";
            for(let i of options){
                htmlCode += `<option>${i}</option>`
            }
            $(`#${id}`).html(htmlCode);
        }
    })
}