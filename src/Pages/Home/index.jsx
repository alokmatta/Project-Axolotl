import {useRef, useState} from "react";

function HomePage () {
  const [previousPrompts, setPreviousPrompts] = useState([])
  const inputRef = useRef()
  
  const [weather, setWeather] = useState('sunny') // sunny, windy, breezy, humid, dry
  const [season, setSeason] = useState('summer') // summer, winder, autumn, spring
  const [temperature, setTemperature] = useState(25) 
  const [crowd, setCrowd] = useState(5) // number of people around
  
  const dynamic = 'It is raining outside. The temperature is 21C. Date is May 29 2021. There are 15 persons looking at me.'
  
  const gpt3 = (input) => {
    let pastConversation = ''
    let index = 0
    const pastPrompts = Array.from(previousPrompts).reverse()
    for (const prompt of pastPrompts){
      index++
      if (index === 1){ 
        continue
      }
      if (prompt.sentBy === 'bot'){
        pastConversation = pastConversation + 'AI: ' + prompt.text + '\n'
      } else {
        pastConversation = pastConversation + 'Human: ' + prompt.text + '\n'
      }
      if (index > 10){
        break
      }
    }
    fetch(`https://5000-magenta-loon-y9lkb9gs.ws-eu08.gitpod.io/?input_text=${encodeURI('Human: ' + input)}&past_conversation=${encodeURI(pastConversation)}&dynamic=${encodeURI(dynamic)}`).then(async res => {
      return await res.json()
    }).then(res => {
      let promptHistory = previousPrompts
      promptHistory.push({text: res.text, sentBy: 'bot'})
      setPreviousPrompts(Array.from(promptHistory))
    })
  }
  
  const sendPrompt = () => {
    let promptHistory = previousPrompts
    promptHistory.push({text: inputRef.current.value, sentBy: 'me'})
    setPreviousPrompts(Array.from(promptHistory))
    gpt3(inputRef.current.value)
    inputRef.current.value = ''
  }
  
  const handleKey = (e) => {
    if (e.key === 'Enter') {
      sendPrompt()
    }
  }
  
  
  return <>
    <div style={{width: '100%'}}>
      <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNkbniqOXYzXzaaQptg2tHEq2G7ep_BBSr-g&usqp=CAU"/>
    <h1>Talk to BЯYAN</h1>
    <br />
    <div style={{width: '300px', margin: 'auto', textAlign: 'start'}}>
    {previousPrompts.map((prompt, i) => {
      return <div key={i} style={{marginTop: '10px'}}>{prompt.sentBy === 'bot' ? <b>Brian: </b> : <b>You: </b>}{prompt.text}</div>
    })}
    </div> 
    <br/>
    <input ref={inputRef} onKeyDown={handleKey}/>
    <button style={{marginLeft: '6px', marginTop: '10px'}} onClick={sendPrompt}>Send</button>
    </div>
  </>
}

export default HomePage