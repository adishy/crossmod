const comment_input = document.querySelector(".comment_input")
    const check_toxicity_button = document.querySelector(".check_toxicity")
    const results_container = document.querySelector(".result_container")

    function show_result(data, comments){
        results_container.innerHTML = "";
        let count = 0;
        data.forEach((comment_result) => {
            comment_result.comment_body = comments[count];
            count++;
            let result_display = `<div class="result">
                                    <p>Comment: ${comment_result.comment_body}</p>
                                    <p>Agreement Score: ${comment_result.agreement_score}</p>
                                    <p>Norm Violation Score: ${comment_result.norm_violation_score}</p>
                                    <p>Subreddits that would remove this comment:</p>
                                    <ul>
                                        ${ comment_result.subreddits_that_remove.map((subreddit) => { return `<li>
                                                                                                                <a href="http://reddit.com/r/${subreddit}" target="_blank">
                                                                                                                    ${subreddit}
                                                                                                                </a>
                                                                                                              </li>`} ).join("")}
                                    </ul>
                                    <p>Norms violated:</p>
                                    <ul>
                                        ${ comment_result.norms_violated.map((norm) => { return `<li>${norm}</li>`} ).join("")}
                                    </ul>
                                </div>
                                <hr>`

            results_container.innerHTML += result_display;
        })
    }

    function get_result(){
        var comments = comment_input.value.split(";")
        fetch('http://crossmod.ml:8300/api/v1/get-prediction-scores', {
            method: 'POST',
            mode: 'cors', 
            cache: 'no-cache', 
            credentials: 'same-origin', 
            headers: {
            'Content-Type': 'application/json'
            },
            redirect: 'follow', 
            referrerPolicy: 'no-referrer', 
            body: JSON.stringify({ comments: comments, key: 'ABCDEFG' }) 
        }).then((response) => {
            return response.json() 
        }).then((data) => {
            show_result(data, comments);
        });
    }
    
    check_toxicity_button.addEventListener("click", get_result);