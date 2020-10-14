const comment_input = document.querySelector(".comment_input")
const removal_consensus_button = document.querySelector(".check_removal_consensus")
const results_container = document.querySelector(".result_container")

function show_result(data, comments){
    results_container.innerHTML = "";
    let count = 0;
    data.forEach((comment_result) => {
        comment_result.comment_body = comments[count];
        count++;
        let allowed_subreddits = ["politics", 
                                  "AskReddit", 
                                  "science", 
                                  "worldnews", 
                                  "news", 
                                  "explainlikeimfive", 
                                  "relationships", 
                                  "TwoXChromosomes", 
                                  "askscience", 
                                  "leagueoflegends", 
                                  "AskHistorians", 
                                  "Games", 
                                  "PoliticalDiscussion", 
                                  "aww", 
                                  "photoshopbattles"]
        comment_result.subreddits_that_remove = comment_result.subreddits_that_remove.filter((subreddit) => { return allowed_subreddits.indexOf(subreddit) != -1 });

        let result_display = `<div class="result">
                                <p>Comment: <em>${comment_result.comment_body}</em></p>
                                <p class="result_category">Agreement Score:</p>
                                <p class="result_category_description">Proportion of subreddits that would remove the comment</p>
                                <p class="result_value"><b>${comment_result.agreement_score} / 1.0</b></p>
                                
                                <p class="result_category">Norm Violation Score:</p> 
                                <p class="result_category_description">Likelihood that the comment violates macro norms on Reddit</p>
                                <p class="result_value"><b>${comment_result.norm_violation_score} / 1.0</b></p>
                                ${
                                    comment_result.subreddits_that_remove.length ? 

                                    `<p>Examples of subreddits that would remove this comment:</p>
                                        <ul>
                                        ${ comment_result.subreddits_that_remove.map((subreddit) => {
                                                                                                        return `<li>
                                                                                                                <a href="http://reddit.com/r/${subreddit}" target="_blank">
                                                                                                                    ${subreddit}
                                                                                                                </a>
                                                                                                            </li>`} ).join("")} 
                                        </ul>`
                                    : ""                       
                                }
                            </div>
                            <hr>`

        results_container.innerHTML += result_display;
    })
}

function get_result(){
    var comments = comment_input.value.split(";")
    fetch('/api/v1/get-prediction-scores', {
        method: 'POST',
        mode: 'cors', 
        cache: 'no-cache', 
        credentials: 'same-origin', 
        headers: {
        'Content-Type': 'application/json'
        },
        redirect: 'follow', 
        referrerPolicy: 'no-referrer', 
        body: JSON.stringify({ comments: comments, key: 'q6Gev880mAp1KDYbaYprpBiJQ4SAASZf2F2SiBOK' }) 
    }).then((response) => {
        return response.json() 
    }).then((data) => {
        show_result(data, comments);
    });
}

removal_consensus_button.addEventListener("click", get_result);

comment_input.addEventListener("keyup", function(event){
    if(event.keyCode == 13){
        get_result();
    }
})

