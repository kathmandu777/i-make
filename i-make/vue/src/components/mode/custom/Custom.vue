<template>
    <div>
        <div class="keypad">
            <div v-if="!selectedPartKind" class="choices-page">
                <Choices :choiceList="partKinds" @update="setPart">
                    <template v-slot:default="{choice}">
                        <img :src="choice.thumbnail_path_for_frontend" width="200" height="200" />
                    </template>
                </Choices>
            </div>
            <div v-else class="choices-page">
                <CustomChoices :partKind="selectedPartKind" @update="pushFacepaints"></CustomChoices>
            </div>

            <img class="key-0 card" v-shortkey.once="[0]" @shortkey="goToMenu()" @click="goToMenu" src="/dist/home.png"
                width="400" height="200">

            <button v-if="!!selectedPartKind" class="key-dot card" v-shortkey.once="['.']" @shortkey="goToParts()"
                @click="goToParts">Parts</button>
        </div>
    </div>
</template>

<script>
import Choices from '@/components/shared/Choices.vue'
import CustomChoices from './CustomChoices.vue';
export default {
    name: "CustomMode",
    data: function () {
        return {
            partKinds: [],
            selectedPartKind: null,
            selectedFacepaints: [],
        };
    },
    methods: {
        async getPartKinds() {
            this.partKinds=await window.eel.get_part_kinds()();
        },
        goToMenu() {
            this.$emit("update-component", "Menu");
        },
        setPart(partKind) {
            if (partKind)
                this.selectedPartKind=partKind;
        },
        pushFacepaints(facepaint) {
            if (facepaint)
                this.selectedFacepaints.push(facepaint);
            this.selectedPartKind=null;
            this.confirm();
        },
        goToParts() {
            this.selectedPartKind=null;

        },
        async confirm() {
            await window.eel.set_effect_image(this.selectedFacepaints)();
            await window.eel.start();
        },
    },
    mounted: function () {
        this.getPartKinds();
    },
    components: { Choices, CustomChoices }
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

.choices-page {
    grid-row: 2/6;
    grid-column: 2/5;
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
