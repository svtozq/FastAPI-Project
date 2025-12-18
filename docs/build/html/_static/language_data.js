/*
 * French Stemmer and Stopwords for searchtools.js
 * Modernized version using let/const
 */

// ---------------------------
// Stopwords français
// ---------------------------
const stopwords = [
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
// BaseStemmer - version modernisée
// ---------------------------
class BaseStemmer {
    constructor() {
        this.current = '';
        this.cursor = 0;
        this.limit = 0;
        this.limit_backward = 0;
        this.bra = 0;
        this.ket = 0;
    }

    setCurrent(value) {
        this.current = value;
        this.cursor = 0;
        this.limit = this.current.length;
        this.limit_backward = 0;
        this.bra = this.cursor;
        this.ket = this.limit;
    }

    getCurrent() {
        return this.current;
    }

    copy_from(other) {
        this.current = other.current;
        this.cursor = other.cursor;
        this.limit = other.limit;
        this.limit_backward = other.limit_backward;
        this.bra = other.bra;
        this.ket = other.ket;
    }

    in_grouping(s, min, max) {
        if (this.cursor >= this.limit) return false;
        let ch = this.current.charCodeAt(this.cursor);
        if (ch < min || ch > max) return false;
        ch -= min;
        if ((s[ch >>> 3] & (1 << (ch & 7))) === 0) return false;
        this.cursor++;
        return true;
    }

    in_grouping_b(s, min, max) {
        if (this.cursor <= this.limit_backward) return false;
        let ch = this.current.charCodeAt(this.cursor - 1);
        if (ch < min || ch > max) return false;
        ch -= min;
        if ((s[ch >>> 3] & (1 << (ch & 7))) === 0) return false;
        this.cursor--;
        return true;
    }

    out_grouping(s, min, max) {
        if (this.cursor >= this.limit) return false;
        let ch = this.current.charCodeAt(this.cursor);
        if (ch < min || ch > max) { this.cursor++; return true; }
        ch -= min;
        if ((s[ch >>> 3] & (1 << (ch & 7))) === 0) { this.cursor++; return true; }
        return false;
    }

    out_grouping_b(s, min, max) {
        if (this.cursor <= this.limit_backward) return false;
        let ch = this.current.charCodeAt(this.cursor - 1);
        if (ch < min || ch > max) { this.cursor--; return true; }
        ch -= min;
        if ((s[ch >>> 3] & (1 << (ch & 7))) === 0) { this.cursor--; return true; }
        return false;
    }

    eq_s(s) {
        if (this.limit - this.cursor < s.length) return false;
        if (this.current.slice(this.cursor, this.cursor + s.length) !== s) return false;
        this.cursor += s.length;
        return true;
    }

    eq_s_b(s) {
        if (this.cursor - this.limit_backward < s.length) return false;
        if (this.current.slice(this.cursor - s.length, this.cursor) !== s) return false;
        this.cursor -= s.length;
        return true;
    }

    // find_among et find_among_b peuvent rester en var mais je les convertis en let
    find_among(v) {
        let i = 0, j = v.length;
        let c = this.cursor, l = this.limit;
        let common_i = 0, common_j = 0;
        let first_key_inspected = false;

        while (true) {
            let k = i + ((j - i) >>> 1);
            let diff = 0;
            let common = common_i < common_j ? common_i : common_j;
            let w = v[k];
            for (let i2 = common; i2 < w[0].length; i2++) {
                if (c + common === l) { diff = -1; break; }
                diff = this.current.charCodeAt(c + common) - w[0].charCodeAt(i2);
                if (diff !== 0) break;
                common++;
            }
            if (diff < 0) { j = k; common_j = common; }
            else { i = k; common_i = common; }
            if (j - i <= 1) {
                if (i > 0 || j === i) break;
                if (first_key_inspected) break;
                first_key_inspected = true;
            }
        }

        do {
            let w = v[i];
            if (common_i >= w[0].length) {
                this.cursor = c + w[0].length;
                if (w.length < 4) return w[2];
                let res = w[3](this);
                this.cursor = c + w[0].length;
                if (res) return w[2];
            }
            i = w[1];
        } while (i >= 0);
        return 0;
    }

    find_among_b(v) {
        let i = 0, j = v.length;
        let c = this.cursor, lb = this.limit_backward;
        let common_i = 0, common_j = 0;
        let first_key_inspected = false;

        while (true) {
            let k = i + ((j - i) >> 1);
            let diff = 0;
            let common = common_i < common_j ? common_i : common_j;
            let w = v[k];
            for (let i2 = w[0].length - 1 - common; i2 >= 0; i2--) {
                if (c - common === lb) { diff = -1; break; }
                diff = this.current.charCodeAt(c - 1 - common) - w[0].charCodeAt(i2);
                if (diff !== 0) break;
                common++;
            }
            if (diff < 0) { j = k; common_j = common; }
            else { i = k; common_i = common; }
            if (j - i <= 1) {
                if (i > 0 || j === i) break;
                if (first_key_inspected) break;
                first_key_inspected = true;
            }
        }

        do {
            let w = v[i];
            if (common_i >= w[0].length) {
                this.cursor = c - w[0].length;
                if (w.length < 4) return w[2];
                let res = w[3](this);
                this.cursor = c - w[0].length;
                if (res) return w[2];
            }
            i = w[1];
        } while (i >= 0);
        return 0;
    }

    replace_s(c_bra, c_ket, s) {
        let adjustment = s.length - (c_ket - c_bra);
        this.current = this.current.slice(0, c_bra) + s + this.current.slice(c_ket);
        this.limit += adjustment;
        if (this.cursor >= c_ket) this.cursor += adjustment;
        else if (this.cursor > c_bra) this.cursor = c_bra;
        return adjustment;
    }

    slice_check() {
        return !(this.bra < 0 || this.bra > this.ket || this.ket > this.limit || this.limit > this.current.length);
    }

    slice_from(s) {
        if (this.slice_check()) this.replace_s(this.bra, this.ket, s);
        return true;
    }

    slice_del() { return this.slice_from(""); }
    slice_to() { return this.slice_check() ? this.current.slice(this.bra, this.ket) : ''; }
    assign_to() { return this.current.slice(0, this.limit); }
}

// ---------------------------
// FrenchStemmer modernisé
// ---------------------------
class FrenchStemmer {
    constructor() {
        this.base = new BaseStemmer();
    }

    stem(word) {
        this.base.setCurrent(word);
        // ici appeler les fonctions r_prelude, r_mark_regions, r_standard_suffix...
        return this.base.getCurrent();
    }
}
