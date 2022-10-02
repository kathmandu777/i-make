<template>
    <div>
        <div class="keypad">
            <div v-for="(hsv, index) in currentColorPalette" :key="index" :class="'key' + (index+1)" class="card">
                <input type="radio" :id="index" :value="hsv" v-model="selectedHSV" v-on:change="confirm()"
                    v-shortkey.once="[(index+1)]" @shortkey="confirm(hsv)" />
                <div class="color-sample" :style="{backgroundColor: hsvToRgbCode(hsv)} "></div>
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
    name: 'SkinColor',
    data: function () {
        return {
            hsvPalette: [[]],
            selectedHSV: [0, 0, 0],
            page: 0
        }
    },
    methods: {
        async getHSVPalette() {
            this.hsvPalette=await window.eel.get_hsv_palette()()
        },
        async confirm(hsv) {
            if (hsv)
                this.selectedHSV=hsv
            await window.eel.set_skin_color(this.selectedHSV[0], this.selectedHSV[1], this.selectedHSV[2])()
        },
        setPage(page) {
            if (page<0)
                page=0
            else if (page>Math.floor((this.hsvPalette.length-1)/9))
                page=Math.floor((this.hsvPalette.length-1)/9)
            this.page=page
        },
        goToMenu() {
            this.$emit('update-component', 'Menu');
        },
        hsvToRgbCode(hsv) {
            var h=hsv[0]/60;
            var s=hsv[1]/100;
            var v=hsv[2]/100;
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

.color-sample {
    width: 230px;
    height: 230px;
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
