$(document).ready(function(){
    setTimeout(function(){
        var url = 'http://localhost:5000/periodictable/classifications/';
        var url1 = 'http://localhost:5000/periodictable/standard_states/';
        var url2 = 'http://localhost:5000/periodictable/blocks/';
        var url3 = 'http://localhost:5000/periodictable/groups/';
        var url4 = 'http://localhost:5000/periodictable/periods/';

        $.ajax({
            url: url,
            type: 'GET',
            success: function(response){
                insert_html(response,'classification');
                $.ajax({
                    url: url1,
                    type: 'GET',
                    success: function(response){
                        insert_html(response,'standardState');
                        $.ajax({
                            url: url2,
                            type: 'GET',
                            success: function(response){
                                insert_html(response,'block');
                                $.ajax({
                                    url: url3,
                                    type: 'GET',
                                    success: function(response){
                                        insert_html(response,'group');
                                        $.ajax({
                                            url: url4,
                                            type: 'GET',
                                            success: function(response){
                                                insert_html(response,'period');   
                                            }
                                        })
                                        
                                    }
                                })
                                
                            }
                        })
                        
                        
                    }
                })

            }
        })
    },3000)
})
$(`#classification`).change(function(){
    change_html('#classification');
})
$(`#standardState`).change(function(){
    change_html('#standardState');
})
$(`#block`).change(function(){
    change_html('#block');
})
$(`#group`).change(function(){
    change_html('#group');
})
$(`#period`).change(function(){
    change_html('#period');
})

function change_html(id){
    let text = $(id).val();
    let urls = {
        '#classification': 'http://localhost:5000/periodictable/classification/',
        '#standardState': 'http://localhost:5000/periodictable/standard_state/',
        '#block': 'http://localhost:5000/periodictable/block/',
        '#group': 'http://localhost:5000/periodictable/group/',
        '#period': 'http://localhost:5000/periodictable/period/'
    };
    console.log(text);
    if(text && text !== 'Select a value'){
        
        $.ajax({
            url: urls[id]+text,
            type: 'GET',
            success: function(response){
                let options = response.options;
                let htmlCode = ""
                for(let i of options){
    
                    htmlCode += `<li>${i}</li>`
                }
                htmlCode = `<ul>${htmlCode}</ul>`
                $(`#element_list`).html(htmlCode);
            }
        })
    }

}

function insert_html(response, id){
    let options = response.options;
    let htmlCode = "";
    for(let i of options){
        htmlCode += `<option value="${i}">${i}</option>`
    }
    $(`#${id}`).html(htmlCode);
}
   