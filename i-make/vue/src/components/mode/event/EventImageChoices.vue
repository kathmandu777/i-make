<template>
    <div>
        <div class="container">
            <div v-for="(choiceImagesPath, index) in currentChoiceImagesPaths" :key="index" :class="'key' + (index+1)">
                <label class="card">
                    <input type="radio" :id="index" :value="choiceImagesPath" v-model="selectedChoiceImagesPath"
                        v-on:change="confirm" v-shortkey.once="[(index+1)]" @shortkey="confirm(choiceImagesPath)" />
                    <img :src="choiceImagesPath" width="230" height="230" />
                </label>
            </div>
            <button class="key0 card" v-shortkey.once="[0]" @shortkey="goToMenu" @click="goToMenu">Menu</button>
            <button class=" key-dot card" v-shortkey.once="['.']" @shortkey="setPage(page-1)"
                @click="setPage(page-1)">Back</button>
            <button class=" key-enter card" v-shortkey.once="['enter']" @shortkey="setPage(page+1)"
                @click="setPage(page+1)">Next</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Choice',
    data: function () {
        return {
            choiceImagesPaths: [],
            selectedChoiceImagesPath: "",
            page: 0
        }
    },
    methods: {
        async getChoiceImagesPaths() {
            this.choiceImagesPaths=await window.eel.get_choice_images()()
        },
        async confirm(path) {
            if (path)
                this.selectedChoiceImagesPath=path
            await window.eel.set_skin_color(27.0, 36.0, 100.0)() // TODO: 任意の色を指定できるように
            await window.eel.set_effect_image_from_path(this.selectedChoiceImagesPath)()
            await window.eel.start()
        },
        setPage(page) {
            if (page<0)
                page=0
            else if (page>Math.floor((this.choiceImagesPaths.length-1)/9))
                page=Math.floor((this.choiceImagesPaths.length-1)/9)
            this.page=page
        },
        goToMenu() {
            this.$router.push("/menu")
        }
    },
    computed: {
        currentChoiceImagesPaths() {
            return this.choiceImagesPaths.slice(this.page*9, this.page*9+9)
        }
    },
    mounted: function () {
        this.getChoiceImagesPaths()
    }
}
</script>

<style scoped>
.container {
    display: grid;
    grid-template-columns: 240px 240px 240px 240px;
    grid-template-rows: 60px 240px 240px 240px 240px 60px;
    grid-template-areas:
        ". . . ."
        "key7 key8 key9 key-minus"
        "key4 key5 key6 key-plus"
        "key1 key2 key3 key-enter"
        "key0 key0 key-dot key-enter"
        ". . . .";
}

.card {
    border: 1px solid #ccc;
    border-radius: 5px;
    display: block;
    padding: 0;
    margin: 5px;
}

.card>input {
    display: none;
}

.card:has(input:checked) {
    border: 2px solid #000;
}

.key0 {
    grid-area: key0;
}

.key1 {
    grid-area: key1;
}

.key2 {
    grid-area: key2;
}

.key3 {
    grid-area: key3;
}

.key4 {
    grid-area: key4;
}

.key5 {
    grid-area: key5;
}

.key6 {
    grid-area: key6;
}

.key7 {
    grid-area: key7;
}

.key8 {
    grid-area: key8;
}

.key9 {
    grid-area: key9;
}

.key-minus {
    grid-area: key-minus;
}

.key-plus {
    grid-area: key-plus;
}

.key-enter {
    grid-area: key-enter;
}

.key-dot {
    grid-area: key-dot;
}
</style>
