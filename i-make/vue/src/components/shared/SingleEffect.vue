<template>
    <div>
        <div class="keypad">
            <div v-for="(facepaint, index) in pageFacepaints" :key="page*9+index" :class="'key-' + keyClassNames[index]"
                class="card">
                <input type="radio" :id="page*9+index" :value="facepaint" v-model="selectedFacepaint"
                    v-on:change="confirm()" v-shortkey.once="[keys[index]]" @shortkey="confirm(facepaint)" />
                <img :src="facepaint.thumbnail_path_for_frontend" width="200" height="200" />
            </div>

            <img class="key-0 card" v-shortkey.once="[0]" @shortkey="goToMenu()" @click="goToMenu" src="/dist/home.png"
                width="400" height="200">
            <img v-if="canGoToPrevPage" class="key-1 card" v-shortkey.once="[1]" @shortkey="setPage(page-1)"
                @click="setPage(page-1)" src="/dist/back.png" width="200" height="200">
            <img v-if="canGoToNextPage" class="key-3 card" v-shortkey.once="[3]" @shortkey="setPage(page+1)"
                @click="setPage(page+1)" src="/dist/next.png" width="200" height="200">
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
            page: 0,
            keys: [4, 5, 6, 7, 8, 9, 'numlock', '/', '*'],
            keyClassNames: [
                '4', '5', '6', '7', '8', '9', 'numlock', 'slash', 'asterisk'
            ]
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
        async goToMenu() {
            await window.eel.stop()();
            this.$emit('update-component', 'Menu', { "resetVideoSrc": true })
        }
    },
    computed: {
        pageFacepaints() {
            return this.facepaints.slice(this.page*9, this.page*9+9)
        },
        canGoToPrevPage() {
            return this.page>0
        },
        canGoToNextPage() {
            return this.page<Math.floor((this.facepaints.length-1)/9)
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
    grid-template-columns: 165px 210px 210px 210px 165px;
    grid-template-rows: 15px 210px 210px 210px 210px 210px 15px;
    grid-template-areas:
        ". . . . ."
        ". key-numlock key-slash key-asterisk ."
        ". key-7 key-8 key-9 ."
        ". key-4 key-5 key-6 ."
        ". key-1 key-2 key-3 ."
        ". key-0 key-0 key-dot ."
        ". . . . .";
    ;
}

.key-0 {
    grid-area: key-0;
}

.key-1 {
    grid-area: key-1;
}

.key-2 {
    grid-area: key-2;
}

.key-3 {
    grid-area: key-3;
}

.key-4 {
    grid-area: key-4;
}

.key-5 {
    grid-area: key-5;
}

.key-6 {
    grid-area: key-6;
}

.key-7 {
    grid-area: key-7;
}

.key-8 {
    grid-area: key-8;
}

.key-9 {
    grid-area: key-9;
}

.key-dot {
    grid-area: key-dot;
}

.key-numlock {
    grid-area: key-numlock;
}

.key-slash {
    grid-area: key-slash;
}

.key-asterisk {
    grid-area: key-asterisk;
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
