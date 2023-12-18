
document.addEventListener('DOMContentLoaded',() => {

    let form = document.querySelector('#boggle_form');
    let input = document.querySelector('#boggle_word');
    let $score = $('#score');
    let $timer = $('#timer');

    class Timer{
        constructor(){
            this.seconds = 10;
            this.showTimer();
            this.id = setInterval(this.count.bind(this), 1000);
            this.valid_guesses = [];
            this.total = 0;
        }
        showTimer(){
            $timer.text(this.seconds)

        }
        async count(){
            console.log(this.seconds)
            this.seconds -= 1 
            this.showTimer()
            if(this.seconds === 0){
                clearInterval(this.id)
                await this.endGame()
            }
        }
        async endGame(){
            let res = await axios({method:'post', url: '/gameover', data: {score : this.total}})
        }
        handleClick(){
            if(this.seconds === 0){return}
            else{
                let guess = input.value;
                this.checkWord(guess);
            }
        }

        async checkWord(guess){
            let res = await axios.get('/check_word', {params : {'guess' : guess}});
            if(res.data.result === 'ok'){
                if(this.valid_guesses.includes(guess)){
                    alert('You already guessed that word');
                }
                else{
                alert('that is a valid word');
                this.valid_guesses.push(guess);
                this.total += guess.length;
                $score.text(this.total);
                }
            }
            else if(res.data.result === "not-on-board"){
                alert('that word is not on the board');
            }
            else if(res.data.result === "not-word"){
                alert('that is not a valid word');
            }

        }
    }

    let boggle_timer = new Timer() 
    form.addEventListener('submit',function(e){
        e.preventDefault()
        boggle_timer.handleClick()
    })
})

