$( function() {
    $("#datepicker" ).datepicker();
} );

function startDataPull(){

    var aDate = $("#datepicker").val().split('/');
    var epoch = new Date(aDate[2], aDate[0] - 1, aDate[1]).getTime();
    
    document.getElementById("testout").innerHTML = "Date entered: " + epoch + "<br>";
    document.getElementById("test2out").innerHTML = "Current date: " + Date.now() + "<br>";

    datatosend = epoch.toString()
    result = runPyScript(datatosend);
    placeGraph(result);
}

function runPyScript(input){
    var AJAXtoFlask = $.ajax({
        type: "POST",
        url: "/datapull",
        async: false,
        data: { mydata: input }
    });

    return AJAXtoFlask.responseText;
}

function placeGraph(htmlin) {
    document.getElementById("test3out").innerHTML = "OUTPUT: <br>" + htmlin;
}