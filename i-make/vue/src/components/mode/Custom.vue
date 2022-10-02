<template>
    <div>
        <div class="keypad">
            <div v-if="tab=='color'" class="tenkey-cursor">
                <TenkeyCursor :choiceList="hsvPalette" @update="setHSV">
                    <template v-slot:default="{choice}">
                        <div class="color-sample" :style="{backgroundColor: hsvToRgbCode(choice)} "></div>
                    </template>
                </TenkeyCursor>
            </div>
            <div v-else-if=" tab=='parts'" class="tenkey-cursor">
                <TenkeyCursor :choiceList="dirFacepaints" @update="setFacepaint">
                    <template v-slot:default="{choice}">
                        <img :src="choice.thumbnail_path_for_frontend" width="200" height="200" />
                    </template>
                </TenkeyCursor>
            </div>

            <button class="key0 card" v-shortkey.once="[0]" @shortkey="goToMenu()" @click="goToMenu">Menu</button>
            <button class=" key-dot card" v-shortkey.once="['.']" @shortkey="prev()" @click="prev()">Back</button>
            <button class=" key-enter card" v-shortkey.once="['enter']" @shortkey="next()" @click="next()">Next</button>

            <button class="key-minus card" v-shortkey.once="['-']" @shortkey="setTab('color')"
                @click="setTab('color')">Color</button>
            <button class="key-plus card" v-shortkey.once="['+']" @shortkey="setTab('parts')"
                @click="setTab('parts')">Parts</button>
        </div>
    </div>
</template>

<script>
import TenkeyCursor from '../shared/TenkeyCursor.vue'

export default {
    name: 'Custom',
    data: function () {
        return {
            facepaints: [],
            hsvPalette: [],
            selectedFacepaint: null,
            selectedColor: null,
            selectedFacepaints: [],
            tab: "parts",
        }
    },
    methods: {
        async getChoiceFacepaints() {
            this.facepaints=await window.eel.get_choice_facepaints()()
        },
        async getHsvPalette() {
            this.hsvPalette=await window.eel.get_hsv_palette()()
        },
        setFacepaint(facepaint) {
            if (facepaint)
                this.selectedFacepaint=facepaint
            console.log(`facepaint: ${this.selectedFacepaint.filename}`)
        },
        setHSV(hsv) {
            if (hsv)
                this.selectedColor=hsv
            console.log(`color: ${this.selectedColor} `)
        },
        async next() {
            if (!this.selectedColor) {
                alert("Please select a color.")
                return
            }
            if (!this.selectedFacepaint) {
                alert("Please select a facepaint.")
                return
            }
            this.selectedFacepaint.hsv=this.selectedColor
            this.selectedFacepaints.push(this.selectedFacepaint)
            console.log(`selectedFacepaints: ${this.selectedFacepaints} `)
            this.selectedColor=null
            this.selectedFacepaint=null
            this.tab="parts"
            if (this.selectedFacepaints.length==this.dirs.length) {
                await window.eel.set_effect_image(this.selectedFacepaints)()
                await window.eel.start()
            }
        },
        prev() {
            this.selectedFacepaints.pop()
            console.log(`selectedFacepaints: ${this.selectedFacepaints} `)
        },
        setTab(tab) {
            this.tab=tab
        },
        goToMenu() {
            this.$emit('update-component', 'Menu')
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
        dirs() {
            return Array.from(new Set(this.facepaints.map(facepaint => facepaint.dir)))
        },
        dir() {
            return this.dirs[this.selectedFacepaints.length]
        },
        dirFacepaints() {
            return this.facepaints.filter(facepaint => facepaint.dir==this.dir)
        }
    },
    mounted: function () {
        this.getChoiceFacepaints()
        this.getHsvPalette()
    },
    components: {
        TenkeyCursor
    }
}
</script>

<style scoped>
.keypad {
    display: grid;
    grid-template-columns: 240px 240px 240px 240px;
    grid-template-rows: 15px 210px 210px 210px 210px 210px 15px;
    grid-template-areas:
        ". . . ."
        "tenkey-cursor tenkey-cursor tenkey-cursor key-backspace"
        "tenkey-cursor tenkey-cursor tenkey-cursor key-minus"
        "tenkey-cursor tenkey-cursor tenkey-cursor key-plus"
        "tenkey-cursor tenkey-cursor tenkey-cursor key-enter"
        "key0 key0 key-dot key-enter"
        ". . . .";
}

.tenkey-cursor {
    grid-area: tenkey-cursor;
}

.key0 {
    grid-area: key0;
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

.key-backspace {
    grid-area: key-backspace;
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
    width: 200px;
    height: 200px;
}
</style>
