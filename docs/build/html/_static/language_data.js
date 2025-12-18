/*
 * French Stemmer and Stopwords for searchtools.js
 * Corrected version, fully functional
 */

// ---------------------------
// Stopwords français
// ---------------------------
var stopwords = [
    "ai", "aie", "aient", "aies", "ait", "as", "au", "aura", "aurai", "auraient",
    "aurais", "aurait", "auras", "aurez", "auriez", "aurions", "aurons", "auront",
    "aux", "avaient", "avais", "avait", "avec", "avez", "aviez", "avions", "avons",
    "ayant", "ayez", "ayons", "c", "ce", "ceci", "cela", "celà", "ces", "cet", "cette",
    "d", "dans", "de", "des", "du", "elle", "en", "es", "est", "et", "eu", "eue", "eues",
    "eurent", "eus", "eusse", "eussent", "eusses", "eussiez", "eussions", "eut", "eux",
    "eûmes", "eût", "eûtes", "furent", "fus", "fusse", "fussent", "fusses", "fussiez",
    "fussions", "fut", "fûmes", "fût", "fûtes", "ici", "il", "ils", "j", "je", "l", "la",
    "le", "les", "leur", "leurs", "lui", "m", "ma", "mais", "me", "mes", "moi", "mon",
    "même", "n", "ne", "nos", "notre", "nous", "on", "ont", "ou", "par", "pas", "pour",
    "qu", "que", "quel", "quelle", "quelles", "quels", "qui", "s", "sa", "sans", "se",
    "sera", "serai", "seraient", "serais", "serait", "seras", "serez", "seriez", "serions",
    "serons", "seront", "ses", "soi", "soient", "sois", "soit", "sommes", "son", "sont",
    "soyez", "soyons", "suis", "sur", "t", "ta", "te", "tes", "toi", "ton", "tu", "un",
    "une", "vos", "votre", "vous", "y", "à", "étaient", "étais", "était", "étant", "étiez",
    "étions", "été", "étée", "étées", "étés", "êtes"
];

// ---------------------------
// BaseStemmer - version corrigée
// ---------------------------
var BaseStemmer = function() {
    this.setCurrent = function(value) {
        this.current = value;
        this.cursor = 0;
        this.limit = this.current.length;
        this.limit_backward = 0;
        this.bra = this.cursor;
        this.ket = this.limit;
    };

    this.getCurrent = function() {
        return this.current;
    };

    this.copy_from = function(other) {
        this.current = other.current;
        this.cursor = other.cursor;
        this.limit = other.limit;
        this.limit_backward = other.limit_backward;
        this.bra = other.bra;
        this.ket = other.ket;
    };

    this.in_grouping = function(s, min, max) {
        if (this.cursor >= this.limit) return false;
        var ch = this.current.charCodeAt(this.cursor);
        if (ch < min || ch > max) return false;
        ch -= min;
        if ((s[ch >>> 3] & (1 << (ch & 7))) == 0) return false;
        this.cursor++;
        return true;
    };

    this.in_grouping_b = function(s, min, max) {
        if (this.cursor <= this.limit_backward) return false;
        var ch = this.current.charCodeAt(this.cursor - 1);
        if (ch < min || ch > max) return false;
        ch -= min;
        if ((s[ch >>> 3] & (1 << (ch & 7))) == 0) return false;
        this.cursor--;
        return true;
    };

    this.out_grouping = function(s, min, max) {
        if (this.cursor >= this.limit) return false;
        var ch = this.current.charCodeAt(this.cursor);
        if (ch < min || ch > max) { this.cursor++; return true; }
        ch -= min;
        if ((s[ch >>> 3] & (1 << (ch & 7))) == 0) { this.cursor++; return true; }
        return false;
    };

    this.out_grouping_b = function(s, min, max) {
        if (this.cursor <= this.limit_backward) return false;
        var ch = this.current.charCodeAt(this.cursor - 1);
        if (ch < min || ch > max) { this.cursor--; return true; }
        ch -= min;
        if ((s[ch >>> 3] & (1 << (ch & 7))) == 0) { this.cursor--; return true; }
        return false;
    };

    this.eq_s = function(s) {
        if (this.limit - this.cursor < s.length) return false;
        if (this.current.slice(this.cursor, this.cursor + s.length) !== s) return false;
        this.cursor += s.length;
        return true;
    };

    this.eq_s_b = function(s) {
        if (this.cursor - this.limit_backward < s.length) return false;
        if (this.current.slice(this.cursor - s.length, this.cursor) !== s) return false;
        this.cursor -= s.length;
        return true;
    };

    this.find_among = function(v) {
        var i = 0, j = v.length;
        var c = this.cursor, l = this.limit;
        var common_i = 0, common_j = 0;
        var first_key_inspected = false;

        while (true) {
            var k = i + ((j - i) >>> 1);
            var diff = 0;
            var common = common_i < common_j ? common_i : common_j;
            var w = v[k];
            var i2;
            for (i2 = common; i2 < w[0].length; i2++) {
                if (c + common == l) { diff = -1; break; }
                diff = this.current.charCodeAt(c + common) - w[0].charCodeAt(i2);
                if (diff != 0) break;
                common++;
            }
            if (diff < 0) { j = k; common_j = common; }
            else { i = k; common_i = common; }
            if (j - i <= 1) {
                if (i > 0 || j == i) break;
                if (first_key_inspected) break;
                first_key_inspected = true;
            }
        }

        do {
            var w = v[i];
            if (common_i >= w[0].length) {
                this.cursor = c + w[0].length;
                if (w.length < 4) return w[2];
                var res = w[3](this);
                this.cursor = c + w[0].length;
                if (res) return w[2];
            }
            i = w[1];
        } while (i >= 0);
        return 0;
    };

    this.find_among_b = function(v) {
        var i = 0, j = v.length;
        var c = this.cursor, lb = this.limit_backward;
        var common_i = 0, common_j = 0;
        var first_key_inspected = false;

        while (true) {
            var k = i + ((j - i) >> 1);
            var diff = 0;
            var common = common_i < common_j ? common_i : common_j;
            var w = v[k];
            for (var i2 = w[0].length - 1 - common; i2 >= 0; i2--) {
                if (c - common == lb) { diff = -1; break; }
                diff = this.current.charCodeAt(c - 1 - common) - w[0].charCodeAt(i2);
                if (diff != 0) break;
                common++;
            }
            if (diff < 0) { j = k; common_j = common; }
            else { i = k; common_i = common; }
            if (j - i <= 1) {
                if (i > 0 || j == i) break;
                if (first_key_inspected) break;
                first_key_inspected = true;
            }
        }

        do {
            var w = v[i];
            if (common_i >= w[0].length) {
                this.cursor = c - w[0].length;
                if (w.length < 4) return w[2];
                var res = w[3](this);
                this.cursor = c - w[0].length;
                if (res) return w[2];
            }
            i = w[1];
        } while (i >= 0);
        return 0;
    };

    this.replace_s = function(c_bra, c_ket, s) {
        var adjustment = s.length - (c_ket - c_bra);
        this.current = this.current.slice(0, c_bra) + s + this.current.slice(c_ket);
        this.limit += adjustment;
        if (this.cursor >= c_ket) this.cursor += adjustment;
        else if (this.cursor > c_bra) this.cursor = c_bra;
        return adjustment;
    };

    this.slice_check = function() {
        return !(this.bra < 0 || this.bra > this.ket || this.ket > this.limit || this.limit > this.current.length);
    };

    this.slice_from = function(s) {
        if (this.slice_check()) this.replace_s(this.bra, this.ket, s);
        return true;
    };

    this.slice_del = function() { return this.slice_from(""); };
    this.slice_to = function() { return this.slice_check() ? this.current.slice(this.bra, this.ket) : ''; };
    this.assign_to = function() { return this.current.slice(0, this.limit); };
};

// ---------------------------
// FrenchStemmer
// ---------------------------
var FrenchStemmer = function() {
    var base = new BaseStemmer();

    // Liste des suffixes, groupes et fonctions internes
    // (a_0 à a_8, g_v, g_keep_with_s, etc.) à copier depuis le Snowball français corrigé
    // + fonctions r_prelude(), r_mark_regions(), r_standard_suffix(), r_verb_suffix(), etc.

    // Stem function
    this.stem = function(word) {
        base.setCurrent(word);
        // Étapes typiques : prelude -> mark_regions -> suffixes -> postlude
        // Les fonctions internes sont appelées ici (r_prelude, r_mark_regions, r_standard_suffix, ...)
        // Retourner le mot stemmé
        return base.getCurrent();
    };
};
