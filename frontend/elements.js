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
                                        insert_html(response,'group', true);
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
// $(`#classification`).change(function(){
//     change_html('#classification');
// })
// $(`#standardState`).change(function(){
//     change_html('#standardState');
// })
// $(`#block`).change(function(){
//     change_html('#block');
// })
// $(`#group`).change(function(){
//     change_html('#group');
// })
// $(`#period`).change(function(){
//     change_html('#period');
// })

$('.join').change(function(){
    let join1 = $(`#classification`).val();
    let join2 = $(`#standardState`).val();
    let join3  = $(`#block`).val();
    let join4 = $(`#group`).val();
    let join5 = $(`#period`).val();
    let selectedOptions = {}
    if(!(join1 === "Select a value" || !join1)){
        selectedOptions["#classification"] = join1;
    }
    if(!(join2 === "Select a value" || !join2)){
        selectedOptions["#standardState"] = join2;
    }
    if(!(join3 === "Select a value" || !join3)){
        selectedOptions["#block"] = join3;
    }
    if(!(join4 === "Select a value" || !join4)){
        selectedOptions["#group"] = join4;
    }
    if(!(join5 === "Select a value" || !join5)){
        selectedOptions["#period"] = join5;
    }
    let selectedKeys = Object.keys(selectedOptions);
    if(selectedKeys.length === 1){
        change_html(selectedKeys[0]);
    }
    else{
        console.log(selectedKeys);
        get_html(selectedOptions);
    }
})

function get_html(jsonData){
    $.ajax({
        url: "http://localhost:5000/periodictable/multiSelect/",
        type: 'POST',
        data: jsonData,
        dataType: "json",
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

$('#element_list').on('click', 'li', function(e){
    let element = e.target.innerText;
    $.ajax({
        url: 'http://localhost:5000/periodictable/element/'+element,
        type : 'GET',
        success : function(response){
            let options = response.options;
            $('#element_details').html(`<p>${JSON.stringify(options)}</p>`);
        }
    })
})

function insert_html(response, id, group){
    let options = response.options;
    let htmlCode = "";
    for(let i of options){
        let value = i;
        if(group){
            value = i.replace( /\D/g, '');
        }
        htmlCode += `<option value="${value}">${i}</option>`
    }
    $(`#${id}`).html(htmlCode);
}
   