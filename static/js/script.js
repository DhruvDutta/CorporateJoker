document.getElementById('upload').addEventListener('click',function(){
    let query = document.getElementById('query').value;
    let div = document.createElement('div')
    div.setAttribute('class','rt');
    div.innerHTML=`<div>${query}</div>`;
    document.getElementById('query').value='';
    document.getElementById('msgbox').appendChild(div);
    $.ajax({
        type: "POST",
        url: '/',
        data: {
            'data':query,
        }, // serializes the form's elements.
        success: function(response)
        {
            response=JSON.parse(response)
            let res = response['output'];
            let div = document.createElement('div')
            div.setAttribute('class','lt');
            div.addEventListener('click',function(){
                speak(div);
            })
            div.innerHTML=`<div>${res}</div>`;
            document.getElementById('query').value='';
            document.getElementById('msgbox').appendChild(div);
        }
    });
})

function speak(ele){
    var msg = new SpeechSynthesisUtterance(ele.children[0].innerText);
    window.speechSynthesis.speak(msg); 
}

function random(){
    $.ajax({
        type: "POST",
        url: '/',
        data: {
            'data':'random',
        }, // serializes the form's elements.
        success: function(response)
        {
            response=JSON.parse(response)
            let res = response['output'];
            let div = document.createElement('div')
            div.setAttribute('class','lt');
            div.addEventListener('click',function(){
                speak(div);
            })
            div.innerHTML=`<div>${res}</div>`;
            document.getElementById('query').value='';
            document.getElementById('msgbox').appendChild(div);
        }
    });
}

document.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
            let query = document.getElementById('query').value;
            let div = document.createElement('div')
            div.setAttribute('class','rt');
            div.innerHTML=`<div>${query}</div>`;
            document.getElementById('query').value='';
            document.getElementById('msgbox').appendChild(div);
            $.ajax({
                type: "POST",
                url: '/',
                data: {
                    'data':query,
                }, // serializes the form's elements.
                success: function(response)
                {
                    response=JSON.parse(response)
                    let res = response['output'];
                    let div = document.createElement('div')
                    div.setAttribute('class','lt');
                    div.addEventListener('click',function(){
                        speak(div);
                    })
                    div.innerHTML=`<div>${res}</div>`;
                    document.getElementById('query').value='';
                    document.getElementById('msgbox').appendChild(div);
                }
            });
    }
    
});