<template>
    <div>
        <div class="keypad">
            <div v-for="(partKind, index) in pagePartKinds" :key="index" :class="'key-' + keyClassNames[index]"
                class="card">
                <input type="radio" :id="index" :value="partKind" v-model="selectedPartKind" v-on:change="confirm()"
                    v-shortkey.once="[keys[index]]" @shortkey="confirm(partKind)" />
                <img :src="partKind.thumbnail_path_for_frontend" width="200" height="200" />
            </div>

            <img class="key-0 card" v-shortkey.once="[0]" @shortkey="goToMenu()" @click="goToMenu" src="/dist/home.png"
                width="400" height="200">
            <img class="key-1 card" v-shortkey.once="[1]" @shortkey="setPage(page-1)" @click="setPage(page-1)"
                src="/dist/back.png" width="200" height="200">
            <img class="key-3 card" v-shortkey.once="[3]" @shortkey="setPage(page+1)" @click="setPage(page+1)"
                src="/dist/next.png" width="200" height="200">
        </div>
    </div>
</template>

<script>
export default {
    name: 'CustomMode',
    data: function () {
        return {
            partKinds: [],
            selectedPartKind: [],
            page: 0,

            // UI
            keys: [4, 5, 6, 7, 8, 9, 'numlock', '/', '*'],
            keyClassNames: [
                '4', '5', '6', '7', '8', '9', 'numlock', 'slash', 'asterisk'
            ]
        }
    },
    methods: {
        async getPartKinds() {
            this.partKinds=await window.eel.get_part_kinds()()
        },
        async confirm(partKind) {
            if (partKind)
                this.selectedPartKind=partKind
            this.$emit('update-component', 'CustomChoices', this.selectedPartKind)
        },
        setPage(page) {
            if (page<0)
                page=0
            else if (page>Math.floor((this.partKinds.length-1)/9))
                page=Math.floor((this.partKinds.length-1)/9)
            this.page=page
        },
        goToMenu() {
            this.$emit('update-component', 'Menu')
        }
    },
    computed: {
        pagePartKinds() {
            return this.partKinds.slice(this.page*9, this.page*9+9)
        }
    },
    mounted: function () {
        this.getPartKinds()
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
