import { useState } from "react";
import "./App.scss";
import { COLORS } from "./config/colors";

function App() {
  const [poem, setPoem] = useState(
    `शब्दों से परे-परे
मन के घन भरे-भरे

वर्षा की भूमिका कब से तैयार है
हर मौसम बूंद का संचित विस्तार है
उत्सुक ॠतुराजों की चिंता अब कौन करे

पीड़ा अनुभूति है वह कोई व्यक्ति नहीं
दुख है वर्णनातीत संभव अभिव्यक्ति नहीं
बादल युग आया है जंगल हैं हरे-हरे

मन का तो सरोकार है केवल याद से
पहुँचते हैं द्वार-द्वार कितने ही हादसे
भरी-भरी आँखों में सपने हैं डरे-डरे`
  );
  const [result, setResult] = useState({});
  const [mode, setMode] = useState("intra_paragraph");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setPoem(e.target.value);
  };

  const handleSubmit = async () => {
    setLoading(true);
    const res = await fetch("http://localhost:5000/rhyme", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ poem }),
    });
    const data = await res.json();
    setLoading(false);
    console.log(data);
    setResult(data?.poem);
  };

  const _poem = []; // array or paragraphs
  const paragraphs = poem.split("\n\n");
  for (let i = 0; i < paragraphs.length; ++i) {
    let para = paragraphs[i];
    const lines = para.split("\n");
    const _lines = [];
    for (let j = 0; j < lines.length; ++j) {
      const line = lines[j];
      const words = line.split(" ").map((w) => ({ text: w, class: w.length }));
      _lines[j] = words;
    }
    _poem[i] = _lines;
  }

  return (
    <div className="App">
      <main>
        <div className="container">
          <div className="input">
            <h1>Poem Input</h1>
            <div className="form">
              <textarea
                name="poem"
                id="poem"
                value={poem}
                onChange={handleChange}
                cols="36"
                rows="20"
                placeholder="Write your poem here..."
                disabled={loading}
                className={loading ? "disabled" : ""}
              ></textarea>
              <button
                onClick={handleSubmit}
                className={loading ? "active" : ""}
              >
                Submit
              </button>
            </div>
          </div>
          <div className="results">
            <div className="ctrl">
              <button
                onClick={() => setMode("intra_paragraph")}
                className={mode == "intra_paragraph" ? "active" : ""}
              >
                Within para
              </button>
              <button
                onClick={() => setMode("inter_paragraph")}
                className={mode == "inter_paragraph" ? "active" : ""}
              >
                Between para
              </button>
            </div>
            {loading && <div className="statusBar"></div>}
            {!loading && result?.[mode] && (
              <div className="data-available-bar"></div>
            )}
            <div className="overlay">
              {result?.[mode]?.map((paragraph, i) => (
                <div className="paragraph">
                  {paragraph.map((line, j) => (
                    <div className="line">
                      {line.map((word, k) => (
                        <div
                          className="word"
                          id={"w" + i + "-" + j + "-" + k}
                          key={"w" + i + "-" + j + "-" + k}
                        >
                          <div
                            style={{
                              background: COLORS[word.class % COLORS.length],
                            }}
                            className="bg"
                          ></div>
                          <div className="text">{word.text}</div>
                        </div>
                      ))}
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
