import json
from django.core.management.base import BaseCommand
from quests.models import Quest, Tag

class Command(BaseCommand):
    help = 'Import quests from a JSON file'

    def handle(self, *args, **kwargs):
        quests_data = [
            {
                "id": 1,
                "title": "Take a photo with Sensoji Temple",
                "tags": ["Asakusa", "Culture", "Free"],
                "description": "Take a photo while making a wish in front of the giant lantern at Sensoji Temple",
                "location": "https://maps.app.goo.gl/KYvmih4HyYcL2Qzi9?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczOEigdUx6i1sSez81UV-WJSXoSZpbtd-KZshCNwCzfZM_jVMZyxVt6JoGcba4tPD8RnFlq1jrLQDPPIIgdmxVBVO-ww4DBpEdpQ3SxIGxDBGcx0hSvi5xmMlwiIXMT2TTGy-AfroKdzg2oLBQuYQdou=w640-h410-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 2,
                "title": "Take a video from the top of the Tokyo",
                "tags": ["Asakusa", "Scenery"],
                "description": "Record a video of Tokyo's scenery from the observation deck of Tokyo Skytree",
                "location": "https://maps.app.goo.gl/tW3AaBhgxrZrofNQ8?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczN4XC-s_AybaqwYAeJu5KcWnRSv2lK21fauZ--aiyyYr8guNRUWes5qV1SgM7WmTGDginVAZOERkYz9N-Fq63lfn0vYUrufDhFPODVfc_wiwYF2lQiXCdIYXJF4mVnMqp-gCRI_9SSMmPS5GJRjbIRL=w615-h410-s-no-gm?authuser=0",
                "badget": "1800JPY"
            },
            {
                "id": 3,
                "title": "Take video at Shibuya crossing",
                "tags": ["Shibuya", "Scenery", "Free"],
                "description": "Record a video of crossing Shibuya Crossing",
                "location": "https://maps.app.goo.gl/ngt1TWKzxP1QtYkZ6?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPz4la6QKArPzP6Vo8-vP3JLCCfzzTX0DZnYqMaXp96wVymoFYlmmVucNSENarmuFiXSHWyHTIpKmU32c2WwsNM0GaYbWVCI2DKD55idIWapGLCMATXwfn1xPqhCmyH2ssvAfV8YNNyMbOF5zxhO6be=w540-h360-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 4,
                "title": "Take a photo with Harajuku Crepe",
                "tags": ["Harajuku", "Food"],
                "description": "Take a photo while eating a crepe on santa monica crepes harajuku",
                "location": "https://maps.app.goo.gl/o2L7SHHc19QRf9wG8",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMP53dstTromi9D6jzMIWhZ20JBLUK-vMkaBTrDvx1UxuUPb7Jx5eDsXYAruFbzd1Nbg2jRLj_3QQKxA_c5-bXLaIzQRyhmHvhDdauGtiopBTHQAwvuKW2JI6ZF7Ofi9mR5QXj3ITq4cWxNA1OH5WjZ=w678-h452-s-no-gm?authuser=0",
                "badget": "600JPY"
            },
            {
                "id": 5,
                "title": "Do toasting with local in Golden Gai",
                "tags": ["Shinjuku", "Night Life"],
                "description": "Record a video of toasting in a bar in Golden Gai, Shinjuku",
                "location": "https://maps.app.goo.gl/gdFwBPF5atRfj2C76?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMeGfIQHJl_ZVPTzm9krv4JRmjcPb1EpMznppm5KyeVWs0KkHnHz57t8rRKylEcb39GSoGSuHjHgzw0WpyeynRdlr5NRUDuSTO9nkmie4FCsmXGlIqe5Usts2vYkS4oBSN1ShbTpLLEiCnSW0J20Qj4=w510-h339-s-no-gm?authuser=0",
                "badget": "3000JPY"
            },
            {
                "id": 6,
                "title": "Take a photo with bridge in imperial palace",
                "tags": ["Imperial Palace", "Scenery", "Free"],
                "description": "Take a photo in front of the Nijubashi Bridge in the Imperial Palace East Garden",
                "location": "https://maps.app.goo.gl/6pvo6UJyneLUbWQ26?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczNoXJS5KToRdbaolV0g0AUrYyWOTuV1oLTnaRpKDhH2U27d2Z-bJpwOYIFQ-X-Op_SpJrGKpwvXwxBwswEPNEFbZHw1AeNj593UgIw0oy3CY2G-COKs8Y-3jkJip5DeR70BhaFztv2wXhpq7TYhjqi4=w510-h339-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 7,
                "title": "Take a photo with Gundam statue",
                "tags": ["Odaiba", "Anime", "Free"],
                "description": "Pose and take a photo with the Gundam statue in Odaiba",
                "location": "https://maps.app.goo.gl/SVhMnYb1Pwu4yzMj8?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPu8qSG8UmN1LseddJFwW4Cn-tT2Qwy4gGNL3EssxNjsteZwi4nuJZFUby1MoSTC-DjybdBPMSMC_N_tRBBR2ixATLjTOdEmB3tIg95DJ-OeCEgaJeVcfbSyPx3ry2QkI9aoHfx55xl9Foef91Q6dE7=w612-h408-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 8,
                "title": "Enjoy fresh seafood at Tsukiji",
                "tags": ["Tsukiji", "Food"],
                "description": "Record a video eating fresh seafood at Tsukiji Market",
                "location": "https://maps.app.goo.gl/TM6y91tR8fy6Ecpq7?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczNlNPBh_8L9NnZhVlO8GhN5m4Fbmv2hIQjV6FqE7oSwhT2MHwJzKbGT6mKJhmjH1mVUo2-iHP0NCxawi5THWOLyN-92bMr1ehE0xRNZ1JCzU07NGJsv8wKf_3efAmk2O6IKwaTgSq_JTKnuc7rP4DUd=w454-h340-s-no-gm?authuser=0",
                "badget": "1000JPY"
            },
            {
                "id": 9,
                "title": "Walk through Torii gate at Meiji Shrine",
                "tags": ["Harajuku", "Shrine", "Free"],
                "description": "Record a video walking through the torii gate at Meiji Shrine",
                "location": "https://maps.app.goo.gl/7pLZeBt2fJ1cdwrL8?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMz1U6rsCovG1N12uRq7EyjqFlOT263Kw1Zlwmu6J7DFkcFn2Ofqeb226jImsvf4DJfZ21Ia7c31zXr7DHmg_JG3-h0xLOf0uDmms_-9vbof7ollRxp5LJkAy3aBmd_MmNfHtnUiKHZxLjaksCSgFr9=w612-h408-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 10,
                "title": "Take a photo with Statue of Liberty",
                "tags": ["Odaiba", "Photo Spot", "Free"],
                "description": "Take a photo with same post of the Statue of Liberty in Odaiba",
                "location": "https://maps.app.goo.gl/tdSkBW7aWbdZpbQp6?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczM08hpslr54-25ripMhMPpuEk8z6v9PhrC5U3MYNBGqNOtiFa_bI1w4Bm_S8jmHPNo3s27zOJ0C2BYz7tGd3JnUERwYQv9krWfFfJkPTs5ZmP4KdSF3Th21qYxk4xbG42OqZ6fodttO2_7tPyT6JrZE=w640-h480-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 11,
                "title": "Take a photo in cosplay costume in Akihabara",
                "tags": ["Akihabara", "Anime"],
                "description": "Borrow the cosplay costume from Cosplay Studio Crown and take a photo in Akihabara",
                "location": "https://livejapan.com/en/in-tokyo/in-pref-tokyo/in-akihabara/article-a0000157/",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczNLyFmcSX3005RucpzPQb25RRZdXla9Q1uzJen0axOiTMpW_ITvVUYFKcZ-jtEyFYYEaYcIycos__yHiXLaqveqvmS3gvmmJvd2JygGT7V719V-Bm0DA9MiSjmf6NK5nscGPCV3H-A3UkJYn-bH7UCR=w612-h408-s-no-gm?authuser=0",
                "badget": "3000JPY"
            },
            {
                "id": 12,
                "title": "Take a photo at Ueno Zoo",
                "tags": ["Ueno", "Family"],
                "description": "Take a photo with pandas at Ueno Zoo",
                "location": "https://www.tokyo-zoo.net/zoo/ueno/hours.html",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczM28fQpWIxJPrVnU55tGRy0ssnSTXRNVoIBJd_N3MW-1wU_HUemsTw7pnBUARfiLgUviwxewneUvMuZKJQvUFHPTlKASoHF8JpZMkl24TEteziLfI7Y56EX88RW0N-llx11trBdmO0rw0Oa7CxP2L6Y=w510-h339-s-no-gm?authuser=0",
                "badget": "600JPY"
            },
            {
                "id": 13,
                "title": "Enjoy Nature at Shinjuku Gyoen",
                "tags": ["Shinjuku", "Nature"],
                "description": "Take a photo at Shinjuku Gyoen National Garden",
                "location": "https://maps.app.goo.gl/nuzMKzgrKGThNDKg8?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczO3bJkoklFKrLP5B1KwL80Pl5CmLykdidaN7sq4FiYlEee1uFmHzTBTgSFmrSUuRsaQq3YR008p1SfZNAvWAxSX2igC9BDu8QwaO-SdxUX46X-L_YOPMJCeZ-Od1pqBtkZFT9VxjvcjJbLynpqcl_LK=w757-h405-s-no-gm?authuser=0",
                "badget": "500JPY"
            },
            {
                "id": 14,
                "title": "Take a video with Dolphin show",
                "tags": ["Ikebukuro", "Family"],
                "description": "Record a video of the dolphin show at Sunshine Aquarium in Ikebukuro",
                "location": "https://maps.app.goo.gl/FHjbPVvDhbArfH4P7?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPw-Q4X3mnoCKMR_wJMAeA93rQg70AQhmJz2ZUeAZqFrOhDUPqrFasMsvZXDrhw-_HPPD_-QrRfrjHoAwm_Zo2XyWAt9VLCNKR6PsgeCVg7mqEsdlLYDfSkWKjOsXjuX9YyUgwx2vdjwbLYRxHsy7nc=w454-h340-s-no-gm?authuser=0",
                "badget": "2600~2800JPY"
            },
            {
                "id": 15,
                "title": "Do shopping at a luxury store in Ginza",
                "tags": ["Ginza", "Shopping"],
                "description": "Record a video shopping at a luxury department store in Ginza",
                "location": "https://maps.app.goo.gl/NyL2eBYpTwe9RWSu8?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczObvPLnjTzqTdHOSQzkciXmubKFhxwKK-XCgcaGR1lwjJ_6LNBbVUDSFCNp-ds3l9FGTsd4Z1Rv2MPgeCFzehuh5uOebI7NnVwGye0nPdv0w9yL6ZIAlAAOayLjCT3LIke6WVysu61u962gewZRs0Q-=w510-h339-s-no-gm?authuser=0",
                "badget": "10000JPY~"
            },
            {
                "id": 16,
                "title": "Take a video on Nakamise Street in Asakusa",
                "tags": ["Asakusa", "Culture"],
                "description": "Record a video buying souvenirs on Nakamise Street in Asakusa",
                "location": "https://maps.app.goo.gl/gRyAA5Uf131dwdXE6?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMvWasJKoj0TfQVkNSEU2f7VtBZe7HlQq5siaYe5KfZSvlq8P9nhr4g4axePw17rgoVf5hPBpA5M0enwVhPYsPNIYz-5l3mbmc7efg1Md6mN9jipBEZpL_4gSCMcVVo5aVC8hvT_qgQgOOoY5m7ZqgL=w510-h339-s-no-gm?authuser=0",
                "badget": "Depends"
            },
            {
                "id": 17,
                "title": "Take a night view photo in Roppongi",
                "tags": ["Roppongi", "Scenery"],
                "description": "Take a night view photo from the observation deck of Roppongi Hills & Museum inside",
                "location": "https://maps.google.com/?q=%E3%80%92106-0032%20%E6%9D%B1%E4%BA%AC%E9%83%BD%E6%B8%AF%E5%8C%BA%E5%85%AD%E6%9C%AC%E6%9C%A8%EF%BC%96%E4%B8%81%E7%9B%AE%EF%BC%91%EF%BC%90%E2%88%92%EF%BC%91%20%E5%85%AD%E6%9C%AC%E6%9C%A8%E3%83%92%E3%83%AB%E3%82%BA%E6%A3%AE%E3%82%BF%E3%83%AF%E3%83%BC%2052%E9%9A%8E%20%E5%85%AD%E6%9C%AC%E6%9C%A8%E3%83%92%E3%83%AB%E3%82%BA%E5%B1%95%E6%9C%9B%E5%8F%B0%20%E6%9D%B1%E4%BA%AC%E3%82%B7%E3%83%86%E3%82%A3%E3%83%93%E3%83%A5%E3%83%BC&ftid=0x60188b770edd442b:0x667ab47030771257&entry=gps&lucs=,94224825,94227247,94227248,47071704,47069508,94218641,94203019,47084304,94208458,94208447&g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMvNScBztBAJNYZtPf20jcefHWPmXoFej0qQxB-UPLXbhyJsE44MiOKD9528O4IzNaurS_piDKkIzILbemhSE_kR-Ej3oEW5ib2b_ONebzJ2vLaMi9L5mPBtVo-FxrvLgpOVY6P9drEmDtSiGEPIOOZ=w510-h339-s-no-gm?authuser=0",
                "badget": "2600JPY"
            },
            {
                "id": 18,
                "title": "Enjoy the boat in Inokashira Park, Kichijoji",
                "tags": ["Kichijoji", "Nature"],
                "description": "Record a video rowing a boat in Inokashira Park, Kichijoji",
                "location": "https://maps.app.goo.gl/6UeGk5BSxqiPRqQ69?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczO-ntehTR_6PgYsuYU6omf3aAbjvLX5cz2Yxg8gvVlZ5biipGKHjrMtKvOB0jfLmXQgmwZce4F11PByFjpK1_JLmKBjAU5a6JPz4SrYhTm79Cze6TItNdJ4DWeGqn-fHeI1ECC_7Ebm0CoT5b4YqHIA=w510-h339-s-no-gm?authuser=0",
                "badget": "600JPY"
            },
            {
                "id": 19,
                "title": "Take a photo from below the Tokyo Tower",
                "tags": ["Asabu", "Scenery", "Free"],
                "description": "Take a photo looking up from the base of Tokyo Tower",
                "location": "https://maps.app.goo.gl/aUmtsF9Sw52ZKeMq5?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczNeoQX5_WQCGIfQNEACYOWZg7nUM7J05abvIneJqmg-41iK9wx7rkQ_fbU2hfT_ruINivXup6WVgeRWfeLD336WQqF3uSkJ_aUlwk_kyzGKtxuVIXraR83nGkixr7pvDfaFEbYGi_oYlqQKjrt0RZDl=w679-h452-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 20,
                "title": "Take a video of local market in Aoyama",
                "tags": ["Shibuya", "Local Experience"],
                "description": "Record a video buying local produce at Aoyama Farmers Market",
                "location": "https://maps.google.com/?q=%E3%80%92150-0001%20%E6%9D%B1%E4%BA%AC%E9%83%BD%E6%B8%8B%E8%B0%B7%E5%8C%BA%E7%A5%9E%E5%AE%AE%E5%89%8D%EF%BC%95%E4%B8%81%E7%9B%AE%EF%BC%95%EF%BC%93%E2%88%92%EF%BC%97%EF%BC%90%20%E9%9D%92%E5%B1%B1%E3%83%95%E3%82%A1%E3%83%BC%E3%83%9E%E3%83%BC%E3%82%BA%E3%83%9E%E3%83%BC%E3%82%B1%E3%83%83%E3%83%88%EF%BC%88Farmers%20Market%20@UNU",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPjkYpjERHvHsuFaSUQ0MMdfbxp9MHtgxVRK1kJx-FxQd32tr_1PiOsoZivUBoXLA3xO8yZPsvea8XH076LnoifYfMizZn1iMYMUcle1wr5nndWI7fAj_G4dXl1IROCN0UBF5tI0wisCcnA5YK6dUCl=w636-h482-s-no-gm?authuser=0",
                "badget": "Depends"
            },
            {
                "id": 21,
                "title": "Enjoy traditional cobblestone alleys in Kagurazaka",
                "tags": ["Kagurazaka", "Local Experience", "Free"],
                "description": "Take a photo on the cobblestone alleys of Kagurazaka (Hyogo Yokocho, Kakurenbo Yokocho, Geisha Koji)",
                "location": "https://www.enjoytokyo.jp/article/108638/",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMYAcSH3moIlfdHlyZzkSKtdHSFAZR3xioDDFlNrLf7TImOgEc-_v77NnNW2CdMS4YbzJ-OABC6UaF3qu-ahB8H0NdjgmjSKTKFXF3YBEQx5NwgKrL0Y7qTO6N0PWEYQ2oMFd0RItFpslt6IY7a4L37=w640-h480-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 23,
                "title": "Take a photo in front of the Wako Clock Tower in Ginza",
                "tags": ["Ginza", "Photo Spot", "Free"],
                "description": "Take a photo in front of the Wako Clock Tower in Ginza",
                "location": "https://maps.app.goo.gl/q1poWpLAhX9P6Gm86?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczP10ugR8-tk6l4dR3MSaOe2JkeNepiOoQ1nsUi4EyWC4tE_wGai1bHxTN4MsRnGO-fwP8fI_YLkmwrYH5GT19ECFZ7hM-A3bQWDhnOg2sUFFPwS6FQvvDg7-qyJ-aBk3X55bTYQzijzqhCW8n49VSdf=w500-h332-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 24,
                "title": "Enjoy Honganji architecture in Tsukiji",
                "tags": ["Tsukiji", "Architecture", "Free"],
                "description": "Take a photo of the unique architecture of Tsukiji Honganji Temple",
                "location": "https://maps.app.goo.gl/2WPTyUFt778c34VS8?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPFTVCiao3VcTktNmK2r7HXI-n2SXfU7DrnqqwXYrp0oO_qk7xiZlgm_hJ0LlS4xyQvAvO8Ucl28cWfBEIR3XbgOhSWQ7_aTtOHHeX0RzSjb_lhkNK9O5tua3qVuanEZkz9LtqUWavv6UYQ_6AVAX2E=w620-h339-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 25,
                "title": "Enjoy beautiful Yoyogi Hachiman Shrine",
                "tags": ["Yoyogi", "Culture"],
                "description": "Record a video praying at Yoyogi Hachiman Shrine",
                "location": "https://maps.app.goo.gl/Zw6qLtjSszN9uXx9A?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPLi210DO6CJVEzPhBPlmKGuTL-nsDUiDU-K24p4PShVKIs4Wb3DbFqDHOsSM9ZWrQZdrP2unkt8SZXLfT6CSIlPs8H9UKmGpVz1GKRpxZ9075OmCYEjseUtGZhLwu7qTIaCMQDe6zEq5cfY4QEdmEG=w510-h339-s-no-gm?authuser=0",
                "badget": "5JPY"
            },
            {
                "id": 26,
                "title": "Enjoy Fish Market in Toyosu",
                "tags": ["Toyosu", "Food"],
                "description": "Record a video of fresh fish being prepared at Toyosu Market",
                "location": "https://maps.app.goo.gl/hKo7DCUPBHVna35XA?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczNTofVIeDBt0aTEQaofH2xInbz0YgH_vCII0gkhBWK6JBgzY7iBQcwq09Ph2oIVq4ncbFk8MnHsIo-W9Td224MsGklHuZBqp4tatEj2ebgnuMkjfm_6kO-j1icjso_0HjDWg4zUfaTtXv7ZfRbBwbAt=w508-h340-s-no-gm?authuser=0",
                "badget": "Depends"
            },
            {
                "id": 27,
                "title": "Take a photo at Center Gai in Shibuya",
                "tags": ["Shibuya", "Photo Spot", "Free"],
                "description": "Take a photo at Center Gai in Shibuya",
                "location": "https://maps.app.goo.gl/u5FmXrvVnKQsLdp89?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPn99tKOhbT6ZIIpPNPtNNsiesxC2ZzxAleuWLTOmid63tjE65vD6Lcw93wMEyYM8omXwTT45pvgHSb8dlLEmV9IjUiXpNwJ6jjGrVWTdsENrUSwKrNQjgwOXBMoMYqs52CnwHfwtZuxTer9rzOlXQd=w510-h339-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 28,
                "title": "Enjoy Tokyo’s night view from Ikebukuro",
                "tags": ["Ikebukuro", "Scenery"],
                "description": "Record a video of the Tokyo skyline from the Sunshine 60 observation deck in Ikebukuro",
                "location": "https://maps.app.goo.gl/H18575hKhjh7DKf38?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczNjOXkj-rXhKtf9_ThnU-GmIJoVc1L7FlI1gY6JzpeO4XbrLKzQH10POS2liYdiRsCg52G7kPpNefcOKmB8FfEIv_fTNB936eKxevb73pU5yQSyxJiSfRtzulvU3mitewRN1UzcdSM1cM3iAedN6z0k=w508-h340-s-no-gm?authuser=0",
                "badget": "700~1200JPY"
            },
            {
                "id": 29,
                "title": "Enjoy Tokyo’s ocean view from Ferris wheel at Kasai",
                "tags": ["Kasai", "Scenery"],
                "description": "Take a photo of the view from the Ferris wheel at Kasai Rinkai Park",
                "location": "https://maps.app.goo.gl/oiPZWxseNgS1945B9?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMJBmifGq0Zugtr9rNPvCDtvHvsVVp2S1nMxsNVixOfj-nLi0bISzfz1VEnkyU8poau9yKTg5laq-RwTe10hh-GTyzAQtMVQ9fZain9X7wrqVQLRfrLtVg6ahQqEfNi7zRVaYFFlnhT8eEGkOw6DrPW=w454-h340-s-no-gm?authuser=0",
                "badget": "800JPY"
            },
            {
                "id": 30,
                "title": "Enjoy beautiful Ebisu Garden Place",
                "tags": ["Ebisu", "Photo Spot", "Free"],
                "description": "Take a photo of night light in Ebisu Garden Place",
                "location": "https://maps.app.goo.gl/zm4QoyzGcKEU9AnC9?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczO0sa4afMnL1PvFBwxO0puwFVG4dsdB8hHNOMoXJVe2cRiBWxVirkKS85sXEcBQUOYIFsMllR6f6ST9K7wCt6eNFyHYuDEUYIRyanS3F5kM8kvo-MWNXA-6zlmngd32R1K8qqfXEDy5rYm7SI7CpdEp=w694-h442-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 31,
                "title": "Ride a rickshaw in Asakusa",
                "tags": ["Asakusa", "Culture"],
                "description": "Record a video riding a rickshaw in Asakusa",
                "location": "https://maps.app.goo.gl/Frse4LxpbQWkAhoS6?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPXLKSlRf7cLCUKLCK3GRXwjcQm6K4GssJyxCN7eOsW9h6SdTn8OVSInhCYTFUwmckwq-jpoaUI8Tdkk5y6CfDKejhDlmuoS62tYOYsg7mOE8rcAqcKi5BnF1Z8AfOaCaaaLCM4SezThKO-kTo_fMli=w679-h452-s-no-gm?authuser=0",
                "badget": "4000JPY~"
            },
            {
                "id": 32,
                "title": "Take a photo with the Moyai statue in Shibuya",
                "tags": ["Shibuya", "Photo Spot", "Free"],
                "description": "Take a photo with the Moyai statue in Shibuya",
                "location": "https://maps.app.goo.gl/xNJTjyqaRShDMnMi7?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczN00jD-7c-vwZ3YP6RXvN9O4mIFO2uLH0ioqdt-uBJbAPE_IMDXO793_t4aVLctV6kiWdLLz0GZMcWE-AbTlNx3iP90ZpHxCqdwCYeA21nqd-5tdH6lq-idDa-qC7VoUmbGhOl3IERCcug0MkOJ7OCH=w678-h452-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 33,
                "title": "Enjoy traditional architecture of Tokyo Station",
                "tags": ["Tokyo", "Architecture", "Free"],
                "description": "Take a photo in front of the Marunouchi Station Building at Tokyo Station",
                "location": "https://maps.app.goo.gl/e8CWi42iy3Pf1QQ46?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPS6VO96O64utL_b-T1XQjYkMjQ-o2XxWXstIi7qvlC7RS3tBQHWu1WOGwVdxuN28j9PZIb44Xk4nEEzHTdnqqLB8J9oj-QvRC-DFLJkRAqTr_DXZRJai0t0QjDiHQ2ML4oKfeJA71LUYkSysWDovL4=w454-h340-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 34,
                "title": "Enjoy glass architecture of Tokyo International Forum",
                "tags": ["Tokyo", "Architecture", "Free"],
                "description": "Take a photo in the glass building of the Tokyo International Forum",
                "location": "https://maps.app.goo.gl/Mt16zyqmqj43u3ka6?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPKnp8YiYQ2WJ417ZjuY36SgTsIdsyhjOihdjtky0rq4DLaSz7OWEVLVqok0LrTxF8Qfc4OgIZ062VSTfMH0m1aRoSb3nL-fdfMsC6GixEIAhgFsZEIU-jNsuLKqi7W5oFzoZOPsbcp4JO3MfHvqrrK=w538-h360-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 35,
                "title": "Enjoy Akihabara’s Maid culture",
                "tags": ["Akihabara", "Anime"],
                "description": "Take a photo with a maid at a maid cafe in Akihabara",
                "location": "https://maps.app.goo.gl/cyw5Hj9RaUnGoMD18?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczNC-FbjtBkPO_DYHtN2iURyJ7-5aEoDI2LIrs-N6t68jfQT7wRiA2v9hFOWj_ttdjmzYV6v_1n4dR2J5beqzntK2PNfXmtEjKDuSkLTYXdQ3dag3tZlVVocRogS25rtmLA6iOaXcFY4IhuxcDO23h2i=w655-h468-s-no-gm?authuser=0",
                "badget": "1500JPY~2500JPY"
            },
            {
                "id": 36,
                "title": "Take a photo at Sukiyabashi Crossing in Ginza",
                "tags": ["Ginza", "Photo Spot", "Free"],
                "description": "Take a photo at Sukiyabashi Crossing in Ginza",
                "location": "https://maps.app.goo.gl/SoC6AVvQCv2UELk39?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPHI0dzakJx0J_s7_Cj8uk3P719nYo3PIseFn0CVqGPd2W7-ICilvD0Gg3YnTDwFSlgPrTfTacRaoWZvR0BqlVgQHVWHq_ur8asmJvF2mYH5_e2I-nF9HtPzKc7o5hqQrJ5wcTRyChQ4kQZ7BVr6IvP=w686-h447-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 37,
                "title": "Enjoy Tokyo’s amusement park inside of city",
                "tags": ["Suidobashi", "Family"],
                "description": "Take a video of yourself riding the roller coaster at Tokyo Dome City",
                "location": "https://maps.app.goo.gl/3mfY364KDCzPz4q9A?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczNgE7HeaTazL-f9Le4Bd5CsNinE7pZhQvvV_Qm2zetelrkbMrjDGhcCME36al7JBMKvkScoUk4k1O3FjkdlLZ-VheqbT2jbYILYpje0hLIanKtaqp6oSjCMXAX0HW20iiF1F6k2OSnoFLoqRlbGU_By=w469-h654-s-no-gm?authuser=0",
                "badget": "Depends"
            },
            {
                "id": 38,
                "title": "Enjoy night view of Tokyo from Shinjuku for free",
                "tags": ["Shinjuku", "Scenery", "Free"],
                "description": "Photograph the view from the observation deck of the Tokyo Metropolitan Government Building in Shinjuku",
                "location": "https://maps.app.goo.gl/kKjS2zNQ6xNRikkp7?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMgltM6rQszQtS8LDqDbsj9CTIvkQnTESisdKfAP7TwW3fgTqeXh3I4w6IMaFT1AKc5vPY_iofCaExBKH2dQBFmydZ6dinwhDSP-yL2ZSz3MREnsrKXlxk5G6KUwU6QgI4QitxSjqgFkWxCMSVPRAQv=w606-h339-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 39,
                "title": "Take a small break at Nakameguro with book and coffee",
                "tags": ["Nakameguro", "Pause", "Cafe"],
                "description": "Take a photo of yourself drinking coffee and reading a book at Tsutaya Bookstore in Nakameguro",
                "location": "https://maps.app.goo.gl/tNGmdZR35e63u5nK7?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMEtfn-wMs0aHwMWZSN5h27Lmnm_pOmucmigfqO5c4LzWLSgcO8bB61QC3IJkka4hdSjN5V_YH866gwl9o6IFbhJlF90o-cdFG9idzR41AkcsfL1Obic1xkrPODA_29AttkiT1MIyH-MvVK7MlHvR1m=w679-h452-s-no-gm?authuser=0",
                "badget": "500JPY"
            },
            {
                "id": 40,
                "title": "Enjoy local shopping area in Ginza",
                "tags": ["Ginza", "Local Experience"],
                "description": "Take a video of yourself shopping at Yanaka Ginza Shopping Street",
                "location": "https://maps.app.goo.gl/HqHscFQKv1xkk8xs6?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczOhIcbhutvOwDqN4gnK9Nk0qIAR4BwgSkRiaXp_14TinCgNyoKmTlbEFwrfG9mYz5_ExXPLCEWcZo7eKUnw1V7YXgtxvC9QWDfzdknux4qdlE0R-UrZ6qyd6zbcv8K_oUeEe0jf2e-IFSflxvTUc9uV=w357-h450-s-no-gm?authuser=0",
                "badget": "Depends"
            },
            {
                "id": 41,
                "title": "Enjoy refreshment walk along Sumida-river",
                "tags": ["Asakusa", "Free"],
                "description": "Take a photo while walking along Sumida River from Sensoji Temple to Tokyo Sky Tree",
                "location": "https://maps.app.goo.gl/3V8TxZhLPNURyycP7?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczOd9_Sdbn9zmnmnYZjwicC0lvvyP7Tqrljxd-IwmRAKac73NvjeHB8mnWJ7667Ms481kqt9Lnfy5BTewT6EqrIud-pgQqPoW58p41Uhe4uI6VdyUITuOPEUA7TTk6kwvSUjGt0mRNAOxLUJ_Q8N3ix0=w678-h452-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 42,
                "title": "Take a video with train at Yoyogi",
                "tags": ["Yoyogi", "Photo Spot", "Free"],
                "description": "Take a video with train and railroad crossing at Yoyogi",
                "location": "https://maps.app.goo.gl/E2CSHLet5FQg3z8R8?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMpSexnVI3-1vxYua0ZfUgbzqOMJ9ni5aq-CQ0DzoCnZk6FJBie2W5xyHhnPIrK8hwHVnr3ZpClYHVEVlKezApFKohvktlWiFO5qd59o_IcxexvLfJkOS_ypzJmp4A9p4jvbwq-5jY-GJLhARaqEwHt=w798-h1558-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 43,
                "title": "Enjoy light art at TeamLab",
                "tags": ["Azabu", "Family"],
                "description": "Record a video experiencing light art at teamLab Borderless in Odaiba",
                "location": "https://maps.app.goo.gl/gtrFd6BN6UJTN4qa8?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczO9N1_12GGqJbnb82UmGvWdWNwr6Wks6atx2mWkTdFyc6vsi_AwtDm58wMDZkL3IH8vM2l1O9thmUxkogXZ6t3fbTxdkp5cI_WvSjmPoUrdCY-3Xbu3bMrJqdYPwDgwYfvvnyT0BbJcxzxu9Bhd25SB=w540-h360-s-no-gm?authuser=0",
                "badget": "3800JPY"
            },
            {
                "id": 44,
                "title": "Enjoy Tokyo teenager style clothing culture",
                "tags": ["Harajuku", "Fashion", "Free"],
                "description": "Take a fashion snap photo on Cat Street in Harajuku",
                "location": "https://maps.app.goo.gl/9RPdHJKEFoHWdky16?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczOqpqZwwC2bhn19NDFeuw3wAq-m_h0-oAGPTztGgKGi-MI6MWcdxciTr5BJ01nD31K3734iMeC8KgQ_toCpZDi0zOp1yUNj4TJ4fe8RxhyZ4ktjmPTTfhk_huK-LJMtyla-Wrgb1ijBm30hOvSKrR__=w606-h339-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 45,
                "title": "Enjoy Tokyo modern Art in Akasaka",
                "tags": ["Akasaka", "Art", "Free"],
                "description": "Record a video appreciating art at Tokyo Midtown in Akasaka",
                "location": "https://maps.app.goo.gl/V3S5woQAjzTWSks28?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMC1fgUwWxll7KWyE1KZNHbZJzSEZ9Sa-92DQaW-XtplCjkNX6nEDBBB2uI1PmqMrnBfg2xLvkm6K-JC_gqc607OoaM8xYKqFSN8KxiCj-Ygw9Qv7xr69QFHrn3wCWFhz7EOALgB8R9_gm10ep1kl9s=w372-h280-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 46,
                "title": "Take a small break at rooftop garden in Ginza",
                "tags": ["Ginza", "Nature", "Free"],
                "description": "Take a relaxing photo in the rooftop garden of Mitsukoshi in Ginza",
                "location": "https://maps.app.goo.gl/svmi9kGD3dsGxbvw5?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczOqOA8lxTdfFt7c8420qxjRdKlpfaP69V-xZzuePtTk32AGSLavsn7HFACHqR7hCLnOUSj8Ut4Flcnz6urmqi-NkjiPT9QikxphtguMvV246ziDrvX3RTqOGrnmEA2lv-qrY1thO5VLBaLYeVkVgrF5=w678-h452-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 47,
                "title": "Enjoy Shinto Culture in Asakusa",
                "tags": ["Asakusa", "Culture"],
                "description": "Record a video praying at Asakusa Shrine",
                "location": "https://maps.app.goo.gl/RYuQE86zTZGgs6Hm6?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczP1CaXLMH1thEay50a6Gd3E8jvZiTtjgloVVBpoVtzV1DKeQq8OwsV_vQZMy2YcbPg8kHegAwAGiPKJYGpa-3jGistqank5DX-LP48sfEtlY3AfbOwdYP8tdYNa3mXjgnCa8Hr9GdGx3sbvZFJiQ3WP=w510-h339-s-no-gm?authuser=0",
                "badget": "5JPY"
            },
            {
                "id": 48,
                "title": "Take a small break with nature near Tokyo Station",
                "tags": ["Tokyo", "Free", "Nature"],
                "description": "Take a relaxing photo in the rooftop garden of the Tokyo Kotsu Kaikan in Yurakucho",
                "location": "https://maps.app.goo.gl/636zvuhm5nF4N6jr9?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczNPWGzUEApCVb79gJfZlAk4tACQ4fdvtLUNLV0pIFAQJOKYoVR8dk5Zqxj0qb4XAfitsBzl01B_lT9ky1EsvIOph03JlC44PUDo0EcKOkTyuURgb6t7yLx_Yqjvq5yc9WIXpSVFH3WM_fk0Lajzbu7X=w678-h452-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 49,
                "title": "Enjoy dolphin show in Shinagawa",
                "tags": ["Shinagawa", "Family"],
                "description": "Record a video of the dolphin show at Aqua Park Shinagawa",
                "location": "https://maps.app.goo.gl/36iSAtXsLEbrEW9a6?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczOQq_XyDBiQwrlSCNIiiIB0cQbX2gIiRkqTBulkzdePpeZZnS93lvoe6kjSza6KMseVZGpmHU64w6WuL47RzFN6RRl6b1gmX40RDCu-x3tjCZWD65tKTH7LTSkbss31LtSx8i5xnb7JNc1VI7ZHWtz2=w450-h319-s-no-gm?authuser=0",
                "badget": "Adult 2500yen child (7-15) 1300yen child(4-6) 800yen Under 4 free"
            },
            {
                "id": 50,
                "title": "Enjoy street food in Ameyoko, Ueno",
                "tags": ["Ueno", "Food"],
                "description": "Record a video buying food from street stalls in Ameyoko, Ueno",
                "location": "https://maps.app.goo.gl/pX44RvZPNGLVRcqM8?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczN-L5gfeg9ZTaITW-PvT2BPV-4RmRsQP2zSzJxTp5RV0DGSNjRNYOA4VhJ4maAM6zSmLswruvAF3mqnBE1uBRNxYZuB53Pk_CRHu4ImciHgqwOTXJzUkWOUhL4LtoQIiU2WrY0FhwUloj7a9vLU78s=w679-h452-s-no-gm?authuser=0",
                "badget": "Depends"
            },
            {
                "id": 51,
                "title": "Enjoy most anime related shrine in Akihabara",
                "tags": ["Akihabara", "Anime", "Free"],
                "description": "Record a video praying at Kanda Myojin Shrine",
                "location": "https://maps.app.goo.gl/7NiKcMGmpv8cxhtu9?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczOIyeSVxCMqvoWY4MoHK4w9s393Z3MNE4ioj2ishqYQqhWBxochSl9uA9EFflr7dZJntFeMFEkoTuwmrdVkoD2ClUP1Knm-NVrdEl28BtkK1z5vftOvaPvXGHi9U5Q2sVYrlRwKM61hSJRm4YFJ9Pga=w1704-h1558-s-no-gm?authuser=0",
                "badget": "5yen"
            },
            {
                "id": 52,
                "title": "Enjoy beautiful and relax time near Tokyo Station",
                "tags": ["Tokyo", "Free"],
                "description": "Take a photo at the Kitte Garden at Tokyo Station at night",
                "location": "https://maps.app.goo.gl/6cPFJ95PnmnZ6oZe8?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPpy4KuJ3E563QtNPH4ml9HBjILVEShBnP5E7x--AHUKwMtZiznOOmGdLQKCC3xyOmICU7zo8RnO_IjTLsFqF4VDjTwJapvzEshBfOsW_XV796vhNyvEV-isBJjzkBtvorNNdcWLKh1q_H14r7vhjVH=w679-h452-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 53,
                "title": "Enjoy Science in Tokyo",
                "tags": ["Odaiba", "Family"],
                "description": "Record a video enjoying exhibits at the National Museum of Emerging Science and Innovation (Miraikan) in Daiba",
                "location": "https://maps.app.goo.gl/gNUJhyvk11hka5YV9?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMR23BzbK4PHcZ_bEVI4TMKL94H2I7hyUkRoXdfpSnK07-G4OSNJxSzrvdooqVyZUEHqdJ1wlCFvhAgJcrpvB_mTCpbvMnZBrTG5DsDfUysZrxv-h1ZZYI8Vfdhm4ZSbAnHH32H44EYF7It0NVzeOkV=w480-h640-s-no-gm?authuser=0",
                "badget": "Adult 630yen child(6-18) 210yen under6 free"
            },
            {
                "id": 54,
                "title": "Enjoy night view of Shibuya",
                "tags": ["Shibuya", "Scenery"],
                "description": "Take a photo of the view from the Shibuya Hikarie observation deck",
                "location": "https://nightscape.tokyo/shibuya/shibuya-hikarie/",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczO7MHQ4brcoMTffdTL3VU-OpCuP76AtwnyBysogUGjBHpoiIX75U0WmpkNxFgko04zmS1juJeROaOzzjHbRWSKDJ851PUwTPqxZLF9k2_arJbtqG1TjXFEjvP17_4cho6SqhYLZdu6Bq-GsPdvFjUAE=w679-h452-s-no-gm?authuser=0",
                "badget": "TICKET,WEB Price,Window Price Adults,2,200 yen,2,500 yen Junior High & High School Students,1,700 yen,2,000 yen Elementary School Students,Only available at the window,1,200 yen Preschoolers (3-5 years old),Only available at the window,700 yen"
            },
            {
                "id": 55,
                "title": "Enjoy night life in Kabukicho, Shinjuku",
                "tags": ["Shinjuku", "Free", "Night Life"],
                "description": "Take a photo of the neon lights in Kabukicho, Shinjuku",
                "location": "https://maps.app.goo.gl/oQNn7p2DpUU1udCW9?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMboit7haTIfSba4Bl_JfG6CfAsIdzwFGS5-TtcEJE2qry62c8k2NgkwpUAiiD7ZE2JDcy4b7z2nJuUNBhTVAMMuJqkJEKWVJc_Dx5UEGCyQiNXsKV6mqgWE8Ny0FZ_Li4Lphq9ArVDIhO6jIV-G_EV=w679-h451-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 56,
                "title": "Enjoy luxury shopping in Ginza",
                "tags": ["Ginza", "Shopping"],
                "description": "Record a video shopping at Matsuya Ginza",
                "location": "https://maps.app.goo.gl/17exJsnXWyAqTmKF8?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczOyTbNkm_OZkrtUKSHbxddMoVynNXutnRimO9WjZG6WOdaqnpe4Jnl09SbG7Bw0eWa_BxQ86o1B8nhdcSXAvy13IcJEs0tzcKYuaqz1VMEiRv5LLKkhkLc1xLvfvENiRM959fphwqo8MiYX-6FY7spJ=w490-h340-s-no-gm?authuser=0",
                "badget": "Depends"
            },
            {
                "id": 57,
                "title": "Enjoy Tokyo Art in Ueno",
                "tags": ["Ueno", "Art"],
                "description": "Record a video appreciating art at the Tokyo National Museum in Ueno",
                "location": "https://maps.app.goo.gl/gm9aE2dc4EJeaxCj8?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPFR9KnNxuDtKzMQEU2tcGnfKeBWUuTRo4SNtAkWKV7f7o_acP6MaNN7oF8qea6GAvPtxAwwzHTHXcXYCvAxDzCJXyhdIIsDO3Hvhw9Hq7NBrS6JAKmCHwvTvnrpTYBHwtZmT2XKHkcx9U72W91hlRm=w274-h182-s-no-gm?authuser=0",
                "badget": "Depends Exhibition"
            },
            {
                "id": 58,
                "title": "Try your fortune in Asakusa",
                "tags": ["Asakusa", "Culture"],
                "description": "Record a video drawing a fortune slip (omikuji) at Sensoji Temple in Asakusa",
                "location": "https://maps.app.goo.gl/KYvmih4HyYcL2Qzi9?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPfyR3e5levZ7KPIDYBSh4C-wgrBfhTfxSwToaNV2HMJZEnpL8pzDCglmoQ_VHUBcwCgXayy2V4Mni9f5-eYb3OC7Ou6nk-t9UGqU5YBM9B_UIkw8f5toU-Fa0K_yUlk6K46mmWItDmFP9AXQZhiLbb=w678-h452-s-no-gm?authuser=0",
                "badget": "100yen"
            },
            {
                "id": 59,
                "title": "Take a photo at Spain Slope in Shibuya",
                "tags": ["Shibuya", "Slope", "Free"],
                "description": "Take a photo at Spain Slope in Shibuya",
                "location": "https://maps.app.goo.gl/dJdSvtL4ds4WGeyB8?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPlcGAXblslJ5nzPUhIOVJ7T0yw8LDFmjpfiaR4KZC7D4leJ2X0pnEYhANidKlhZxEsxljFsby3b7-TgEAG25SJvgb_OkhzAih2DTwJ-umPn2kXd0pvjaAndZKSKME3xbkbmhgKFgT8_EpY_M_-1Kb6=w640-h427-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 60,
                "title": "Enjoy beautiful aquarium in Shinagawa",
                "tags": ["Shinagawa", "Family"],
                "description": "Record a video at the Epson Aqua Park Shinagawa",
                "location": "https://maps.app.goo.gl/PotQ2BVC1Nouk9R5A?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczP7TYLM8IXKku6xF4bDsAXhouJuMv2TuqHFpD_QzNgPz1kOB5108VV5a2fcelN0q2cAGqFv5uNMx199Y49MB7HXPET5U8TjH0H6tm1_jUZlagTFS-cvUfmJXOrHHzEz3Fte82yOnHmTrNbZgfPU3YNf=w460-h345-s-no-gm?authuser=0",
                "badget": "2,500yen"
            },
            {
                "id": 61,
                "title": "Enjoy beautiful architecture of Starbucks Reserve in Nakameguro",
                "tags": ["Nakameguro", "Architecture"],
                "description": "Record a video enjoying coffee at Starbucks Reserve Roastery in Nakameguro",
                "location": "https://maps.app.goo.gl/RbLJPRB941pfmzr17?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczNmQkSPoXAZuJlgJb8Re77PcgqdGSEbrKDA7ZxUtB3GFOLp3YAUmXQ5usEMH5mL3nnTA7BiYXZ9sDUlanznHP2-exGEon_uhfliNiyBNpJ6jA8Pg6asSmTUMVK5kiKFArbb4a8t7VAobvfvQaZyDeNI=w678-h452-s-no-gm?authuser=0",
                "badget": "1,000yen-"
            },
            {
                "id": 62,
                "title": "Enjoy Tokyo’s beach with beautiful view",
                "tags": ["Odaiba", "Scenery"],
                "description": "Take a photo by the beach at DECKS Tokyo Beach in ODaiba",
                "location": "https://maps.app.goo.gl/ffy9Uz45Xdq1unRQA?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPRIR7pNumAenshxxvWtiei3o2oegxb4eh1e1gCfTOYV6R2KfaNpSyYiNwBSwkqLTKJyEUj4QE2uMg28fbRJGYWQBjdgSMqeLWhBJhoOXCD_hn91ojeIaJ334NTcxFSNYlXSCBnW71ImHeJc1iT38-w=w510-h339-s-no-gm?authuser=0",
                "badget": "Depends"
            },
            {
                "id": 63,
                "title": "Enjoy Anime culture in Radio Kaikan in Akihabara",
                "tags": ["Akihabara", "Anime"],
                "description": "Record a video searching for anime goods at Radio Kaikan in Akihabara",
                "location": "https://maps.app.goo.gl/LXa9Wn14CTBbd6pf7?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPzcwU82wRenLnNnv6BIIy9AI-9HBX9AHVLsGaV-W3eNheNEmmwNQNbbtPTNC4IX0EZxL8aQNH9zztcSPYfQf2yCFWDhW1ywyYV1Ja4ilui7SEwT_FKxJRX80IhOQw4k6x14nQFNdtfQWIhzdThiV3z=w639-h426-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 64,
                "title": "Enjoy traditional Japanese show in Asakusa",
                "tags": ["Asakusa", "Culture"],
                "description": "Record a video enjoying a rakugo performance at Asakusa Engei Hall",
                "location": "https://maps.app.goo.gl/ZAcC27HZpfU7rK2D7?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczOy1Z-VIhTgCFJVqscTp_3Tmb8X7cLdev47gGqCj2c0OW35WcpyyiovIyGbaclcCpaHrfxMib1xg4VhmetauO83B_f9GX-oC0o1NsEpfHDTD1Q16uYW5HNaUU9Pcc7y83cnfN4joNIkSYTsbxKgoZ7k=w688-h340-s-no-gm?authuser=0",
                "badget": "Adult 3,000yen student 2,500yen Child 1,500yen *At night, the price of adult and student will be discounted by 500yen."
            },
            {
                "id": 65,
                "title": "Enjoy Kimono walking in Asakusa",
                "tags": ["Asakusa", "Culture"],
                "description": "Take a video of walking around Asakusa wearing a yukata. We recommend the store on the link.",
                "location": "https://maps.app.goo.gl/SeLENZDM7No94tyi9?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPL8-5lR3_yWl8PZ9PKFWnzL61xHAfA_iUDZMZZQLbu05YnskyYMzVbKczEY9SD0bgo9XQxyxAVQyUnu8AY4cpsip5twqWmri4tD7kla1MWc7fC1-AOl5d_Z5QY2hCOWQUXmqCzX9hLlqwthHBRlTSO=w540-h360-s-no-gm?authuser=0",
                "badget": "https://ewha-yifu.com/shops/asakusa/yukata-planlist/?utm_source=google&utm_medium=cpc&utm_campaign=tonai&gclid=Cj0KCQjwkdO0BhDxARIsANkNcrf-S-9RpqrNlTvXGPCxmH6OzaFOGC9YApA6nZdAFgsglGisWO0tmVQaAjo-EALw_wcB"
            },
            {
                "id": 66,
                "title": "Enjoy recycle clothing culture in Shimokitazawa",
                "tags": ["Shimokitazawa", "Fashion"],
                "description": "Record a fashion show-like video wearing vintage clothes in Shimokitazawa",
                "location": "https://maps.google.com/?q=%E3%80%92155-0031%20%E6%9D%B1%E4%BA%AC%E9%83%BD%E4%B8%96%E7%94%B0%E8%B0%B7%E5%8C%BA%E5%8C%97%E6%B2%A2%20%E4%B8%8B%E5%8C%97%E6%B2%A2&ftid=0x601821ff675efbc3:0x332e8e1d2d9ec482&entry=gps&lucs=,94224825,94227247,94227248,47071704,47069508,94218641,94203019,47084304,94208458,94208447&g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczP8Vng1yI4tHyo73oO_YQxG_m6vJEjDvGvGOfFJYuqO8kpBLwgL3IGBEl6BjMlOWoEKbJrMDmcbw30RUiMDt1RdVryZGgNJu8tobxqIUW4UvF7h7dzx83fP1QH-Olj97gwjZSCj1BoM0_yQtOOW9b68=w640-h480-s-no-gm?authuser=0",
                "badget": "Free only for try on"
            },
            {
                "id": 67,
                "title": "Make first step to Japan",
                "tags": ["Narita", "Haneda"],
                "description": "Record a video of deboarding an airplane, with or without people",
                "location": "",
                "imgUrl": "",
                "badget": "Free"
            },
            {
                "id": 68,
                "title": "Enjoy Tokyo’s view from boat",
                "tags": ["Tokyo", "Scenery"],
                "description": "Enjoy a ride on a yakatabune (traditional Japanese boat) in Tokyo",
                "location": "https://yakata-fune.jp/search/results/100457",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczOT-Eu16TYOemk_DQcEYbeg-4PQVdhXWtw-m3pE6pyCRBfQsSOt9CGpHrkCGvvmAHhM8BVyVMgm5_rl9M0qIbrRP3-b0iAaQrtUfE6993nOrYqMRzniiXOHpoUI3IfO068uUFEZL6WN1fhdaHHB4SQk=w540-h360-s-no-gm?authuser=0",
                "badget": "https://funayado-mikawaya.smart-change.info/en/"
            },
            {
                "id": 69,
                "title": "Learn Sumo culture in Ryogoku",
                "tags": ["Ryogoku", "Culture"],
                "description": "Learn about sumo culture in Ryogoku",
                "location": "https://maps.app.goo.gl/abDJJPtEYErudwzh6",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMUGqRLnZqtXmLp39JsYpUe4gkKlvhEYJZlOE39exGycyIYNUfnZ9f8kQ1oDV-p3VedMWMb8wjkM3IxPrFWuIAOc0sucIGGoMjr6ykFiwAOBL8q_lAVIRACvfa-iKK8aj4i1teAQq6ZCdSmDuuDslCG=w640-h480-s-no-gm?authuser=0",
                "badget": "https://whereyourebetween.com/destinations/japan/how-to-watch-sumo-training-tokyo/"
            },
            {
                "id": 70,
                "title": "Enjoy Sumo Food in Ryogoku",
                "tags": ["Ryogoku", "Food"],
                "description": "Eat sumo stew (chanko) in Ryogoku",
                "location": "https://maps.app.goo.gl/SaXx4XbsMrXoL8SN8?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPjHfPJ72yCy_iJ1-Dj5YI2WEvPRlj3z18H5AL8zn3-hDuqTyPhNd-s5cSvJdOEbbY4gb_xNvy_cv6LmX8pMDZImVxGTyDdqUwIyXEWCX96kWZ8gwc4gRAv6T9vRxgdlsmuoKgMWW8ns_iSWVEyZh07=w480-h360-s-no-gm?authuser=0",
                "badget": "5000~6000JPY"
            },
            {
                "id": 71,
                "title": "Enjoy traditional Izakaya in Ueno",
                "tags": ["Ueno", "Izakaya", "Night Life"],
                "description": "Drink at Daitoryo-izakaya in Ueno",
                "location": "https://www.google.co.jp/maps/place/%E3%82%82%E3%81%A4%E7%84%BC+%E5%A4%A7%E7%B5%B1%E9%A0%98/@35.7103687,139.7722945,17z/data=!3m1!4b1!4m6!3m5!1s0x60188e9882eb388d:0xa520e94ee40763e4!8m2!3d35.7103644!4d139.7748694!16s%2Fg%2F1tflxwyd?entry=ttu",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczM-GLcZI5JpVvywUqB52d_1N5EXycQpN93MhADOl57TJlsmdp49QkIwwPIaigsnuO9vuTqXpU5aVtFtGuFuSjB-IvCs6mUsExDgK2eFAbowI9Wuppgow1G75xbvm0jlYjPAxS0wxu_8lj7zLikJ00ML=w640-h427-s-no-gm?authuser=0",
                "badget": "1000~3000JPY"
            },
            {
                "id": 72,
                "title": "Enjoy Kabuki show in Ginza",
                "tags": ["Ginza", "Culture"],
                "description": "Enjoy traditional Japanese performing arts at Kabukiza in Ginza",
                "location": "https://maps.app.goo.gl/eJptwrb9GnHz7FE36?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczP_AWZUosb_pBke2nFtC3VjXSXen6dwMLEgIesBaOeH5VCF_9XV6-vr0divlwQut9vXC7QuACSv3-MiktdOGqHdE6PwYgwhNGk6vi1MkZd-zo4rgDBd9TqygKvJrHYam9tXod1Ud2vXkGWcZ8mS82zD=w514-h339-s-no-gm?authuser=0",
                "badget": "3,500-17,000JPY"
            },
            {
                "id": 73,
                "title": "Enjoy Tokyo’s night view from Odaiba",
                "tags": ["Odaiba", "Scenery", "Free"],
                "description": "Take a photo with Tokyo's night skyline at Odaiba Seaside Park",
                "location": "https://maps.app.goo.gl/sc9prU9VnEwKY8sr8?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczNuNFbCDuS6fWWmekN3k1L8q6SeEsjoTo3BFgEmrnpDQZ-9Kc1MVijiUO9eJ9XKZKDV_a16Ob5LxKdDWUOxFm62l1rc9_GK79hXBRAodwUbgN9BnYnuAxdvufbB-yAU4KVHIYnMxW-4zNkW61wU_AKA=w664-h360-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 74,
                "title": "Enjoy Arcade version Mario Kart",
                "tags": ["Family", "Amusement"],
                "description": "Record a video of playing Mario Kart at an arcade",
                "location": "https://maps.app.goo.gl/67xjhspB2CJJW4ZbA?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczOu5rJQ47qUNd1w2yhALWzsAavz_mPPRaX-1uKd-m1vYW1iu4HQp_pMUsVgcLoh9uj3gj8ufaC1PChjQjMa9hRtiijmnNny16RCXW0gPoannaPwLNIxZgAmWeNDOJSXQ6fbttBm3S7mwrF_zrOSt7Fr=w640-h480-s-no-gm?authuser=0",
                "badget": "100JPY"
            },
            {
                "id": 75,
                "title": "Enjoy Crane Game and win a prize",
                "tags": ["Family", "Amusement"],
                "description": "Record a video of playing crane games at an arcade",
                "location": "https://maps.app.goo.gl/67xjhspB2CJJW4ZbA?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMiaF_UiUs-b71UWKmbfNIKSzV5Mu1LKBCbKmMyv_U1De3lVgIStTqLhxdcprHpsKdZF6AdjAb2R5Z5caBQTEdQUcMY4al1EkJHUFZ6uRmlbaipxelnRyW9tsJRO33bvPFcDhK8JHlZQ4wPhGzRh0KC=w544-h962-s-no-gm?authuser=0",
                "badget": "100JPY~"
            },
            {
                "id": 76,
                "title": "Enjoy VR experience in Odaiba",
                "tags": ["Odaba", "Family"],
                "description": "Record a video of experiencing VR at Joypolis in Odaiba",
                "location": "https://maps.app.goo.gl/YS9mS2JtRcKffoXV6?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMPJsVk5SL2ke7ph8irRR-LrF-GnFq31QuKJMvVbJ95C-LEdFjamJ_SOIHOVWVNel9KA-36khp8MbCQ9lkcld4IHrjRp8QCTtAhmULVDx9Iruz3A5Ji43_P1ysB_pIAl5Pi3ukbQVQQG0azUg2WQQR8=w400-h266-s-no-gm?authuser=0",
                "badget": "Admission Ticket - Adults (18 years and older): 1,200 yen - Elementary, Junior High, and High School Students: 900 yen Evening Passport - Includes admission and unlimited attractions (from 15:00, time may change without notice) - Adults (18 years and older): 4,500 yen - Adults (60 years and older): Indoor fee (proof required)"
            },
            {
                "id": 77,
                "title": "Enjoy Pokemon Center in Shibuya",
                "tags": ["Shibuya", "Anime", "Free"],
                "description": "Take a photo posing like Mew-two at the Pokemon Center in Parco",
                "location": "https://maps.app.goo.gl/66EYA5XuycCFHd646?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczNuWoNv_ggmorHIF36KeoepGsCKHQF4k7gGREzTb9JL7bEN2coxtLYP16SZvz1Gy341HGStEQAr50QxwenG0SpCOh1kQsf3ZXzRFEZjQxw6VKQgn5ittMq9QXOKdCxMWfaqLPsC0TMiL-sD3C0W54H2=w627-h836-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 78,
                "title": "Enjoy a famous photo spot among teenagers in Shibuya",
                "tags": ["Shibuya", "Photo Spot", "Free"],
                "description": "Take a photo with the mirror at KOMEHYO in Shibuya",
                "location": "https://maps.app.goo.gl/4eRzPB23J7aN451Q8?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczMrxTdxJGoNYIJn9o1fo0i8-5vZJ7z5-C9GuXckaZvI4QuMdZX9MSG5kju92fIa2RwtGaHQZZ03JWa7YRWErzkfVh7vKqyFHiWv1oMt_RM_oZcBjIbgLlEvhU67SkxaZ0HTTLFO5tAKA0_TZQKNDs8P=w626-h836-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 79,
                "title": "Enjoy Seafood-don at Taneichi, Tsukiji",
                "tags": ["Tsukiji", "Food"],
                "description": "Take a photo with Seafood-don at Taneichi (This is restaurant cheap but high quality)",
                "location": "https://maps.app.goo.gl/hpekv94XhK8vBV698",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPcdHbCfl4bEmuHiS6JZwpAC9nqlb47MjVEA6xdsW5e1gsIJ55FZHbVQsk5IxrZw6PSSWIGOEnOw7MU0cSM8RdJgBNjzWU_c7RBOcjyYT1KL6Ci57CP4juh3cnB_AlpvdJW_LRLGugpv61cHI1gHo1c=w886-h591-s-no-gm?authuser=0",
                "badget": "1000~2000JPY"
            },
            {
                "id": 80,
                "title": "Take a photo with the statue at Sushi Zanmai in Tsukiji",
                "tags": ["Tsukiji", "Photo Spot", "Free"],
                "description": "Take a photo with the statue at Sushi Zanmai in Tsukiji",
                "location": "https://maps.app.goo.gl/DPBSyX7z1qEFpc2v6?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPGfeSxQYokdqvkOzox_HiXcE9W5WGKn_GT5a2VTxWe44IcPigtNO7erFQkQa78o2y8GQpSCDQhgmOQbpBcoxIWR35AacSzuOub-NpQKFNEUIq_rjtSCuCEducCISnoPPDktWAgo2S0YpL-Kk2fm9UE=w480-h640-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 81,
                "title": "Enjoy a wall covered by small windmills in Asakusa",
                "tags": ["Asakusa", "Photo Spot", "Free"],
                "description": "Record a video of blowing on the windmill at the entrance of Nishisando Shopping Street in Asakusa",
                "location": "https://maps.app.goo.gl/KPaoxpiXfy1EnE637?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczNKy6VQ68BXA64U477sYUZt5TbOotRT7muLFiuhl0ulRK6S_UnPeInXJpbHS-MHVH91zT8n9biRFuLPG4f-zUJbje6NBJzxNCN_S8xnCjIR09P_SJYTb106k4lD_C1rN3B19x9Mje9bsZz6ioUtMtes=w627-h835-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 82,
                "title": "Enjoy the traditional arcade in Asakusa",
                "tags": ["Asakusa", "Amusement", "Culture"],
                "description": "Take a video of enjoying the traditional arcade inside Nishisando Shopping Street in Asakusa",
                "location": "https://maps.app.goo.gl/KPaoxpiXfy1EnE637?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczN6aUgP3y9ZnQYINGyMRva2STVF-sm45-SENnERikD7mytJ6DyNZaVyvtqOkBIYMqCgDkFovwr0h2jtyRkiKU4bfBzDCwdEPe3-lSgqYRBrATyPm3kP-UnQWIPOLVstMb5g-24VPs3dykvW4TPHholo=w627-h836-s-no-gm?authuser=0",
                "badget": "Depends"
            },
            {
                "id": 83,
                "title": "Enjoy Anime culture in Akihabara",
                "tags": ["Akihabara", "Free"],
                "description": "Take a photo with your favorite character goods at Radio Kaikan in Akihabara",
                "location": "https://maps.app.goo.gl/LL6pZUzFUTt1yjWC9?g_st=com.google.maps.preview.copy",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczME7-CIpg-7V9lvVRjQ5FfCUri666DtRWYC9nnwLu0UBLKFe1lREXjezD49j38gvZYYT2z97AGqHa0ZCnbu99qhp1kbv1s0W-j-wDhOAlDEgoGKh4j86BGXmPBAg4fu_R3EIEK8EgWhR0UDWG_i36k4=w627-h836-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 84,
                "title": "Enjoy instagramable spot in Harajuku",
                "tags": ["Harajuku", "Photo Spot", "Free"],
                "description": "Take a photo at the mirror section of Tokyu Plaza Omotesando Harajuku",
                "location": "https://www.google.co.jp/maps/place/%E6%9D%B1%E6%80%A5%E3%83%97%E3%83%A9%E3%82%B6%E8%A1%A8%E5%8F%82%E9%81%93%E3%80%8C%E3%82%AA%E3%83%A2%E3%82%AB%E3%83%89%E3%80%8D/@35.6687337,139.70338,17z/data=!3m2!4b1!5s0x60188ca47ed0a4b1:0x3dde7d1ec6b8ca30!4m6!3m5!1s0x60188ca47d9d408f:0xcad336117f4b7838!8m2!3d35.6687294!4d139.7059549!16s%2Fg%2F121qgg5n?entry=ttu",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczNAahsQ449fhy1_dxXgQFtkwH2Qt1wqFh-ZYGdFlUOvp7nJU7W4wGvy_F8ALCg1RcgMOxLE3PR2CPx12O0v8bUOoeaayPhQdEucBCjMepMXGcjAQ5q6rxKdH6jJ7mjxxqCsqLLUF5ZjwNfcJ9JXEqBw=w519-h1009-s-no-gm?authuser=0",
                "badget": "Free"
            },
            {
                "id": 85,
                "title": "Enjoy instagramable spot in Shibuya",
                "tags": ["Shibuya", "Photo Spot"],
                "description": "Take a photo with Shibuya Crossing from Mag’s Park",
                "location": "https://maps.app.goo.gl/vkV14agtvmNxM92E8",
                "imgUrl": "https://lh3.googleusercontent.com/pw/AP1GczPdaFlnhPLkQJ03Z-fEwCumlDW8IBtBf5AHzFSOJYgnCB4V0J5xlrbbUpHyHW6H2cndxxkGsW7LOol9regeBBiWaTjhTvfDyYyECd7-_DhhgTNkrb4hJPsZB7k7nPOV8PdoI4kNjDDtcmg5REg8vyD8=w594-h516-s-no-gm?authuser=0",
                "badget": "1800JPY(including 1 drink)"
            }
        ]
        
        self.save_to_django(quests_data)

    def save_to_django(self, quests):
        for quest_data in quests:
            tags = quest_data.pop("tags")
            quest, created = Quest.objects.get_or_create(**quest_data)
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                quest.tags.add(tag)
            quest.save()