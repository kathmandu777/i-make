<template>
    <div>
        <div class="keypad">
            <div v-for="(hsv, index) in currentColorPalette" :key="page*9+index" :class="'key-' + keyClassNames[index]"
                class="card">
                <input type="radio" :id="page*9+index" :value="hsv" v-model="selectedHSV" v-on:change="confirm()"
                    v-shortkey.once="[keys[index]]" @shortkey="confirm(hsv)" />
                <div class="color-sample" :style="{backgroundColor: hsvToRgbCode(hsv)} "></div>
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
    name: 'SkinColor',
    data: function () {
        return {
            hsvPalette: [],
            selectedHSV: null,
            page: 0,
            keys: [4, 5, 6, 7, 8, 9, 'numlock', '/', '*'],
            keyClassNames: [
                '4', '5', '6', '7', '8', '9', 'numlock', 'slash', 'asterisk'
            ]
        }
    },
    methods: {
        async getHSVPalette() {
            this.hsvPalette=await window.eel.get_hsv_palette()()
        },
        async confirm(hsv) {
            if (hsv)
                this.selectedHSV=hsv
            await window.eel.set_skin_color(this.selectedHSV)()
        },
        setPage(page) {
            if (page<0)
                page=0
            else if (page>Math.floor((this.hsvPalette.length-1)/9))
                page=Math.floor((this.hsvPalette.length-1)/9)
            this.page=page
        },
        async goToMenu() {
            await window.eel.stop()();
            this.$emit('update-component', 'Menu', { "resetVideoSrc": true });
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
        currentColorPalette() {
            return this.hsvPalette.slice(this.page*9, this.page*9+9)
        }
    },
    mounted: function () {
        this.getHSVPalette()
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

.color-sample {
    width: 190px;
    height: 190px;
    border-radius: 60px;
    margin: 4px 6px 6px 4px;
}
</style>
