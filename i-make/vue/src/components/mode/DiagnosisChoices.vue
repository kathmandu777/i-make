<template>
    <div>
        <h2 class="mode">診断モード</h2>
        <h3 class="question">{{question}}</h3>
        <div class="container">
            <div class="choice" v-for="(choice, index) in choices" :key="index">
                <button v-shortkey.once="[(index+1)]" @shortkey="setAnswer(index)" @click="setAnswer(index)"
                    class="css-button-arrow--sky">{{ index+1 }}:
                    {{choice.answer}}</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Choice',
    data: function () {
        return {
            question: '',
            choices: [],
            config: {}
        };
    },
    methods: {
        async getQuestionAndChoices() {
            const res=await window.eel.get_question_and_choices()();
            this.question=res[0];
            this.choices=res[1];
            if (res[0]==this.config.DIAGNOSIS_FINISH_MSG)
                await window.eel.start();
        },
        async setAnswer(index) {
            const res=await window.eel.set_answer(index)();
            if (res==this.config.SET_ANSWER_ERROR_MSG)
                alert(res);
            else
                this.getQuestionAndChoices();
        },
        async getConfig() {
            this.config=await window.eel.get_config()();
        }
    },
    mounted: function () {
        this.getConfig();
        this.getQuestionAndChoices();
    }
}
</script>

<style>
.mode {
    font-size: 64px;
    margin: 30px;
    padding: 0;
}

.question {
    font-size: 128px;
    margin: 0;
    padding: 0;
    text-align: center;
}

.container {
    width: 100%;
    height: 100%;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: space-around;
    gap: 10px;
}

.css-button-arrow--sky {
    width: 100%;
    height: 100%;
    color: #fff;
    padding: 30px 60px;
    font-size: 64px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    display: inline-block;
    outline: none;
    overflow: hidden;
    border-radius: 20px;
    border: none;
    background-color: #3a86ff
}

.css-button-arrow--sky:hover {
    border-radius: 20px;
    padding-right: 24px;
    padding-left: 8px;
}

.css-button-arrow--sky:hover:after {
    opacity: 1;
    right: 10px;
}

.css-button-arrow--sky:after {
    content: "\00BB";
    position: absolute;
    opacity: 0;
    font-size: 64px;
    line-height: 64px;
    top: 32px;
    right: -20px;
    transition: 0.4s;
}
</style>
