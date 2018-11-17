function searchUser(searchKey, groupid) {
	if(searchKey==""){
		document.getElementById('searchedUser').innerHTML="";
		return
	}
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
     		var resp = JSON.parse(this.responseText);
     		console.log(resp);
     		var view = '<ul class="list-group">';
     		for(var i=0;i<resp.length;i++){
     			view+='<li class="list-group-item">'+resp[i]["username"]+' <a href="#" onclick="adduser('+ groupid +','+resp[i]["id"]+',\''+ resp[i]["username"] +'\')">Add</a>';
     		}
     		view+="</ul>"
     		document.getElementById('searchedUser').innerHTML=view;
    	}
  	};
  	xhttp.open("GET", "/splitit/searchforadding/"+groupid+"/"+searchKey, true);
  	xhttp.send();
}

function adduser(groupid, userid, username){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
     		var resp = JSON.parse(this.response);
     		if(resp["response"]=="success"){
     			document.getElementById('closeAddUser').click();
     			var div = document.getElementById('alluseringrpdiv');
     			div.innerHTML+='<div class="panel-body" id="userPannel'+userid+'"> '+username+' <a href="#" onclick="removeUser('+groupid+','+ userid+', \''+username+'\')">Remove</a> '+'</div>';
     			document.getElementById('searchedUser').innerHTML="";
     			document.getElementById('addUsrSearch').value="";
     		}

    	}
  	};
  	xhttp.open("POST", "/splitit/addusertogrp/"+groupid+"/"+userid+"/", true);
  	xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
  	xhttp.send();
}

function removeUser(groupid, userid, username){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
     		var resp = JSON.parse(this.response);
     		if(resp["response"]=="success"){
     			var delDiv = document.getElementById('userPannel'+userid);
     			delDiv.parentNode.removeChild(delDiv);
     		}

    	}
  	};
  	xhttp.open("POST", "/splitit/removeuserfrmgrp/"+groupid+"/"+userid+"/", true);
  	xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
  	xhttp.send();
}

function delgrpConf(groupid){
	document.getElementById('delgrpConfBtn').setAttribute("onclick","delgrp("+groupid+")");
}

function delgrp(groupid){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
    		var resp = JSON.parse(this.response);
    		console.log(resp);
    		if(resp["response"]=="success"){
    			var div = document.getElementById('groupPannel'+groupid);
    			div.parentNode.removeChild(div);
    		}
    	}
  	};
  	xhttp.open("DELETE", "/splitit/delgrp/"+groupid+"/", true);
  	xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
  	xhttp.send();
}

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
     	for (var i = 0; i < cookies.length; i++) {
        	var cookie = jQuery.trim(cookies[i]);
         // Does this cookie string begin with the name we want?
         	if (cookie.substring(0, name.length + 1) == (name + '=')) {
            	 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
             	break;
         	}
     	}
 	}
 	return cookieValue;
}

function settlerequest(transactionId){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
    		location.href='/splitit/';
    	}
  	};
  	xhttp.open("POST", "/splitit/settlerequest/"+transactionId+"/", true);
  	xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
  	xhttp.send();
}

function settle(requestId, transactionId){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        if(this.responseText=="success"){
          location.href='/splitit/';
        }
      }
    };
    xhttp.open("POST", "/splitit/settle/"+requestId+"/"+transactionId+"/", true);
    xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhttp.send();
}