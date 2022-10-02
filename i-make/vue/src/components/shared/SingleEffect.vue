<template>
    <div>
        <div class="keypad">
            <h1 class="title">
                <slot></slot>
            </h1>
            <div v-for="(facepaint, index) in pageFacepaints" :key="index" :class="'key' + (index+1)" class="card">
                <input type="radio" :id="index" :value="facepaint" v-model="selectedFacepaint" v-on:change="confirm()"
                    v-shortkey.once="[(index+1)]" @shortkey="confirm(facepaint)" />
                <img :src="facepaint.thumbnail_path_for_frontend" width="230" height="230" />
            </div>
            <button class="key0 card" v-shortkey.once="[0]" @shortkey="goToMenu()" @click="goToMenu">Menu</button>
            <button class=" key-dot card" v-shortkey.once="['.']" @shortkey="setPage(page-1)"
                @click="setPage(page-1)">Back</button>
            <button class=" key-enter card" v-shortkey.once="['enter']" @shortkey="setPage(page+1)"
                @click="setPage(page+1)">Next</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'SingleEffect',
    data: function () {
        return {
            facepaints: [],
            selectedFacepaint: [],
            page: 0
        }
    },
    methods: {
        async getChoiceFacepaints() {
            this.facepaints=await window.eel.get_choice_facepaints()()
        },
        async confirm(facepaints) {
            if (facepaints)
                this.selectedFacepaint=facepaints
            await window.eel.set_effect_image(this.selectedFacepaint)()
            await window.eel.start()
        },
        setPage(page) {
            if (page<0)
                page=0
            else if (page>Math.floor((this.facepaints.length-1)/9))
                page=Math.floor((this.facepaints.length-1)/9)
            this.page=page
        },
        goToMenu() {
            this.$emit('update-component', 'Menu')
        }
    },
    computed: {
        pageFacepaints() {
            return this.facepaints.slice(this.page*9, this.page*9+9)
        }
    },
    mounted: function () {
        this.getChoiceFacepaints()
    }
}
</script>

<style scoped>
.keypad {
    display: grid;
    grid-template-columns: 240px 240px 240px 240px;
    grid-template-rows: 120px 240px 240px 240px 240px;
    grid-template-areas:
        "title title title title"
        "key7 key8 key9 key-minus"
        "key4 key5 key6 key-plus"
        "key1 key2 key3 key-enter"
        "key0 key0 key-dot key-enter"
    ;
}

.title {
    grid-area: title;
    font-size: 80px;
    line-height: 120px;
    margin: 0;
    padding: 0;
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
</style>
