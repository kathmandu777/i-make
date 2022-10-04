<template>
    <div>
        <div class="top">
            <h2 class="mode">診断モード</h2>
            <img class="menu-button" v-shortkey.once="[0]" @shortkey="goToMenu()" @click="goToMenu"
                src="/dist/home.png">
        </div>
        <h3 class="question">{{question}}</h3>
        <h3 v-if="!choices" class="result">{{result}}</h3>
        <div class="container">
            <div v-if="!choices" class="choice">
                <button class="css-button-arrow--sky" v-shortkey.once="['enter']"
                    @shortkey="setAnswer(config.CALL_FUNC_ID)"
                    @click="setAnswer(config.CALL_FUNC_ID)">次へ(Enter)</button>
            </div>
            <div v-else class="choice" v-for="(choice, index) in choices" :key="index">
                <button v-shortkey.once="[(index+1)]" @shortkey="setAnswer(index)" @click="setAnswer(index)"
                    class="css-button-arrow--sky">{{ index+1 }}:
                    {{choice}}</button>
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
            result: '',
            choices: [],
            config: {}
        };
    },
    methods: {
        async getQuestionAndChoices() {
            const res=await window.eel.get_question_and_choices()();
            this.question=res[0];
            this.choices=res[1];

            if (!this.choices)
                await window.eel.start_diagnosis_func()();
        },
        async setAnswer(index) {
            const res=await window.eel.set_answer(index)();
            if (res==this.config.SET_ANSWER_ERROR_MSG)
                alert(res);
            else if (res==this.config.DIAGNOSIS_FINISH_MSG) {
                this.question="診断終了"
                this.choices=[];
                await window.eel.set_effect_image_by_settings()();
                await window.eel.start();
            }
            else
                this.getQuestionAndChoices();
        },
        async getConfig() {
            this.config=await window.eel.get_config()();
        },
        setResult(value) {
            this.result=value;
        },
        async goToMenu() {
            await window.eel.stop()();
            this.$emit('update-component', 'Menu', { "resetVideoSrc": true })
        }
    },
    mounted: function () {
        window.eel.expose(this.setResult, 'setResult');
        this.getConfig();
        this.getQuestionAndChoices();
    }
}
</script>

<style>
.top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.top>.mode {
    font-size: 64px;
    margin: 30px;
    padding: 0;
}

.top>.menu-button {
    height: 100px;
    width: auto;
}

.question {
    font-size: 70px;
    margin: 0;
    padding: 0;
    text-align: center;
}

.result {
    font-size: 55px;
    margin: 10px 40px;
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
    width: calc(100% - 60px);
    color: #fff;
    padding: 15px 30px;
    margin: 10px 30px;
    font-size: 40px;
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
</style>
