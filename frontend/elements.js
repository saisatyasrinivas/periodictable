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
    let text = $(`#classification`).val();
    console.log(text);
})

function change_html(id){
    console.log($(`${id} option:selected`).text());
}

function insert_html(response, id){
    let options = response.options;
    let htmlCode = "";
    for(let i of options){
        htmlCode += `<option value="${i}">${i}</option>`
    }
    $(`#${id}`).html(htmlCode);
}
   