from hooyootracker.constants import Game, Source


SOURCE_URLS = {
    Game.GenshinImpact: {
        Source.Game8: r"https://game8.co/games/Genshin-Impact/archives/304759",
        Source.PocketTactics: r"https://www.pockettactics.com/genshin-impact/codes",
        Source.RockPaperShotgun: r"https://www.rockpapershotgun.com/genshin-impact-codes-list",
        Source.VG247: r"https://www.vg247.com/genshin-impact-codes",
    },
    Game.ZenlessZoneZero: {
        Source.Game8: r"https://game8.co/games/Zenless-Zone-Zero/archives/435683",
        Source.PocketTactics: r"https://www.pockettactics.com/zenless-zone-zero/codes",
        Source.Polygon: r"https://www.polygon.com/zenless-zone-zero-guides/24191640/zzz-codes-redeem-redemption-gift-polychrome",
        Source.VG247: r"https://www.vg247.com/zenless-zone-zero-codes"
    }
}
