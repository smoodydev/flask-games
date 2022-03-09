function get_pokemon() {
    let the_pokemon = $(`#pokemon_entered`).val().toLowerCase();
    console.log(the_pokemon);
    if (pokemonNames.includes(the_pokemon)) {
        return the_pokemon;
    }
    return false;

}

function make_type_card(types, section) {
    console.log()
    for (let type in types) {
        if (types[type] != "") {
            if (!$("#" + section + " ." + types[type]).length) {
                $("#"+section).append(`<div class="typebadge ${types[type]}">
                ${types[type]}
            </div>`);
            }

        }
    }


}

function make_pokemon_card(the_pokemon) {
    let height, weight = "";
    if (the_pokemon.height[0]){
        height = "Taller"
        $("#tallerThan").html(the_pokemon.height[1]+"m < ")

    }else{
        height = "Shorter"
        $("#shorterThan").html(" > " +the_pokemon.height[1]+"m")
    }
    if (the_pokemon.weight[0]){
        weight = "Heavier"
        $("#heavierThan").html(the_pokemon.weight[1]+"kg < ")
    }else{
        weight = "Lighter"
        $("#lighterThan").html(" > " +the_pokemon.weight[1]+" kg")
    }
    return `
    <div class="c4 md1">
        <img src="static/gifs/${the_pokemon.name.toLowerCase()}.gif"><p>${the_pokemon.name}</p><p>${height}<p><p>${weight}<p>
    </div>`
}

function try_word() {
    let the_pokemon = get_pokemon();
    if (the_pokemon) {
        $.post($SCRIPT_ROOT + '/guess_pokemon', {
            pokemon: the_pokemon
        }, function (data) {
            if (data.validated) {
                pk = data.result;
                
                // wordsent = "";
                // paintCells(data.result, word_attempt);
                // $("#result").text("Result for " + word_attempt);
                // attempt++;
                // letter_index = 0;
                // attempt_array.push(data.result);
                // if (data.result == "y".repeat(num_letters)){
                //     alert("You are a Wiener!")
                //     openWinModal();
                // }
                make_type_card(pk.types, "correctTypes")
                make_type_card(pk.not_types, "guessedTypes")
                if (data.code ==2){
                    $("#thepkimg").attr("src", "static/gifs/"+pk.name.toLowerCase()+".gif");
                    $("#correctHeight").html("Height: "+pk.height+"m")
                    $("#correctWeight").html("Weight: "+pk.weight+"kg")
                }
                else{
                    $("#guessedPokemon").append(make_pokemon_card(pk));
                }
                
                // $("#guessedTypes").append(make_type_card(pk.not_types));
            }
            else {
                $("#result").text(data.text_back);
            }
        });
    }
}

$('#enter').bind('click', function () {
    try_word();
    return false;
});