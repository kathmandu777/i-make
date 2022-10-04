<template>
    <div>
        <div class="choices">
            <div v-for="(choice, index) in pageChoiceList" :key="page*9+index" :class="'key-' + keyClassNames[index]"
                class="card">
                <input type="radio" :id="page*9+index" :value="choice" v-model="selectedChoice"
                    v-shortkey.once="[keys[index]]" @shortkey="confirm(choice)" />
                <slot v-bind:choice="choice"></slot>
            </div>

            <img v-if="canGoToPrevPage" class="key-1 card" v-shortkey.once="[1]" @shortkey="setPage(page-1)"
                @click="setPage(page-1)" src="/dist/back.png" width="200" height="200">
            <img v-if="canGoToNextPage" class="key-3 card" v-shortkey.once="[3]" @shortkey="setPage(page+1)"
                @click="setPage(page+1)" src="/dist/next.png" width="200" height="200">
        </div>
    </div>
</template>

<script>
export default {
    name: 'Choices',
    props: ['choiceList'],
    data: function () {
        return {
            selectedChoice: null,
            page: 0,

            //UI
            keys: [4, 5, 6, 7, 8, 9, 'numlock', '/', '*'],
            keyClassNames: [
                '4', '5', '6', '7', '8', '9', 'numlock', 'slash', 'asterisk'
            ]
        }
    },
    methods: {
        setPage(page) {
            if (page<0)
                page=0
            else if (page>Math.floor((this.choiceList.length-1)/9))
                page=Math.floor((this.choiceList.length-1)/9)
            this.page=page
        },
        confirm(choice) {
            this.selectedChoice=choice
            this.$emit('update', choice)
        },
    },
    computed: {
        pageChoiceList() {
            return this.choiceList.slice(this.page*9, this.page*9+9)
        },
        canGoToPrevPage() {
            return this.page>0
        },
        canGoToNextPage() {
            return this.page<Math.floor((this.choiceList.length-1)/9)
        }
    }
}
</script>

<style scoped>
.choices {
    display: grid;
    grid-template-columns: 210px 210px 210px;
    grid-template-rows: 210px 210px 210px 210px;
    grid-template-areas:
        "key-numlock key-slush key-asterisk"
        "key-7 key-8 key-9"
        "key-4 key-5 key-6"
        "key-1 key-2 key-3";
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

.key-slush {
    grid-area: key-slush;
}

.key-asterisk {
    grid-area: key-asterisk;
}

.key-numlock {
    grid-area: key-numlock;
}

.card {
    border-radius: 5px;
    display: block;
    padding: 0;
    margin: 5px;
}

.card>input {
    display: none;
}

.card:has(input:checked) {
    border: 2px solid lightgreen;
}
</style>
