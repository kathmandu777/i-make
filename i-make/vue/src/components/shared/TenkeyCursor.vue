<template>
    <div>
        <div class="tenkey-cursor">
            <div v-for="(choice, index) in pageChoiceList" :key="index" :class="'key' + (index+1)" class="card">
                <input type="radio" :id="index" :value="choice" v-model="selectedChoice" v-shortkey.once="[(index+1)]"
                    @shortkey="confirm(choice)" />
                <slot v-bind:choice="choice"></slot>
            </div>

            <button class=" key-slush card" v-shortkey.once="['/']" @shortkey="setPage(page-1)"
                @click="setPage(page-1)">←</button>
            <button class=" key-asterisk card" v-shortkey.once="['*']" @shortkey="setPage(page+1)"
                @click="setPage(page+1)">→</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'TenkeyCursor',
    props: ['choiceList'],
    data: function () {
        return {
            selectedChoice: null,
            page: 0
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
        hsvToRgbCode(hsv) {
            var h=hsv.h/60;
            var s=hsv.s/100;
            var v=hsv.v/100;
            if (s==0) return [v*255, v*255, v*255];

            var rgb;
            var i=parseInt(h);
            var f=h-i;
            var v1=v*(1-s);
            var v2=v*(1-s*f);
            var v3=v*(1-s*(1-f));

            switch (i) {
                case 0:
                case 6:
                    rgb=[v, v3, v1];
                    break;
                case 1:
                    rgb=[v2, v, v1];
                    break;
                case 2:
                    rgb=[v1, v, v3];
                    break;
                case 3:
                    rgb=[v1, v2, v];
                    break;
                case 4:
                    rgb=[v3, v1, v];
                    break;
                case 5:
                    rgb=[v, v1, v2];
                    break;
            }
            return "rgb("+parseInt(rgb[0]*255)+","+parseInt(rgb[1]*255)+","+parseInt(rgb[2]*255)+")";
        }
    },
    computed: {
        pageChoiceList() {
            return this.choiceList.slice(this.page*9, this.page*9+9)
        }
    }
}
</script>

<style scoped>
.tenkey-cursor {
    display: grid;
    grid-template-columns: 240px 240px 240px;
    grid-template-rows: 210px 210px 210px 210px;
    grid-template-areas:
        "key-numlock key-slush key-asterisk key-backspace"
        "key7 key8 key9 key-minus"
        "key4 key5 key6 key-plus"
        "key1 key2 key3 key-enter";
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

.color-sample {
    width: 230px;
    height: 230px;
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

.key-slush {
    grid-area: key-slush;
}

.key-asterisk {
    grid-area: key-asterisk;
}

.key-backspace {
    grid-area: key-backspace;
}

.key-numlock {
    grid-area: key-numlock;
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
