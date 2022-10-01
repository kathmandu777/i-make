<template>
    <div>
        <h2>診断モード</h2>
        <h3 text-align="center">{{question}}</h3>
        <div class="container">
            <div class="choice" v-for="(choice, index) in choices" :key="index">
                <button @click="setAnswer(index)">{{choice.answer}}</button>
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
            if (res[0]==this.config.DIAGNOSIS_FINISH_MSG)
                await window.eel.start();
            else {
                this.question=res[0];
                this.choices=res[1];
            }
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
.container {
    width: 100%;
    height: 100%;
    padding: 10px;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    align-content: center;
    justify-content: flex-start;
    gap: 10px;
}
</style>
