<template>
    <div>
        <div class="half-HD">
            <div class="main-content">
                <h2 class="mode">診断モード</h2>

                <h3 class="question">{{ question }}</h3>
                <h3 v-if="!choices" class="response">{{ response }}</h3>
                <div v-if="!!result_text" class="result">
                    <p>{{ result_text }}</p>
                </div>
                <div>
                    <div class="container">
                        <div v-if="!choices" class="choice">
                            <button
                                class="css-button-arrow"
                                v-shortkey.once="['enter']"
                                @shortkey="setAnswer(config.CALL_FUNC_ID)"
                                @click="setAnswer(config.CALL_FUNC_ID)"
                            >
                                次へ(Enter)
                            </button>
                        </div>
                        <div
                            v-else
                            class="choice"
                            v-for="(choice, index) in choices"
                            :key="index"
                        >
                            <button
                                v-shortkey.once="[keys[index]]"
                                @shortkey="setAnswer(index)"
                                @click="setAnswer(index)"
                                class="css-button-arrow"
                            >
                                {{ choice }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <img
                class="menu-button"
                v-shortkey.once="[0]"
                @shortkey="goToMenu()"
                @click="goToMenu"
                src="/dist/home.png"
            />
        </div>
    </div>
</template>

<script>
export default {
    name: 'Diagnosis',
    data: function () {
        return {
            question: '',
            response: '',
            choices: [],
            config: {},
            result_text: null,
            keys: ['/', 8, 5, 2], // 選択肢が4つ以下前提
        }
    },
    methods: {
        async getQuestionAndChoices() {
            const res = await window.eel.get_question_and_choices()()
            this.question = res[0]
            this.choices = res[1]

            if (!this.choices) await window.eel.start_diagnosis_func()()
        },
        async setAnswer(index) {
            const res = await window.eel.set_answer(index)()
            const msg = res[0]
            const result_text = res[1]
            if (msg == this.config.SET_ANSWER_ERROR_MSG) alert(res)
            else if (msg == this.config.DIAGNOSIS_FINISH_MSG) {
                this.question = '診断終了'
                this.choices = []
                this.result_text = result_text
                await window.eel.set_effect_image_by_settings()()
                await window.eel.start_rendering()
            } else this.getQuestionAndChoices()
        },
        async getConfig() {
            this.config = await window.eel.get_config()()
        },
        setResponse(value) {
            this.response = value
        },
        async goToMenu() {
            await window.eel.stop()()
            this.$emit('update-component', 'Menu')
        },
    },
    mounted: function () {
        window.eel.expose(this.setResponse, 'setResponse')
        this.getConfig()
        this.getQuestionAndChoices()
    },
}
</script>

<style>
.half-HD {
    display: grid;
    grid-template-columns: 960px;
    grid-template-rows: 920px 160px;
    grid-template-areas:
        'main-content'
        'menu-button';
}

.main-content {
    grid-area: main-content;
}

.menu-button {
    grid-area: menu-button;
    width: auto;
    height: 160px;
}

.mode {
    font-size: 64px;
    margin: 30px;
    padding: 0;
}

.question {
    font-size: 70px;
    margin: 0;
    padding: 0;
    text-align: center;
}

.response {
    font-size: 55px;
    margin: 10px 40px;
    padding: 0;
    text-align: center;
}

.container {
    width: 100%;
    height: auto;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: space-around;
    gap: 10px;
}

.result {
    font-size: 50px;
    margin: 10px 40px;
    padding: 0;
    white-space: pre-line;
}

.css-button-arrow {
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
    background-color: #66c5a9;
}
</style>
