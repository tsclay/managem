<script lang="ts">
  // Fetch content data on page load and insert into DOM
  const renderImages = async (preResponse = null) => {
    const imageDisplay = searchForOne('div.asset-grid')
    let content

    if (searchTargets) {
      empty(imageDisplay, () => {
        searchTargets = null
      })
    }

    const deleteImage = async (eRef) => {
      const request = {
        method: 'DELETE',
        body: JSON.stringify({
          image_id: parseInt(eRef.value)
        }),
        headers: {
          'Content-Type': 'application/json'
        }
      }
      const response = await fetch('/admin/assets/delete', request).then((r) =>
        r.json()
      )

      renderImages(response)
    }
    const handleNotification = (json, asset) => {
      const cancel = (e) => {
        e.currentTarget.parentElement.remove()
      }
      const confirm = (e) => {
        e.currentTarget.parentElement.remove()
        deleteImage({ value: e.currentTarget.value })
      }
      const exitBtn = createElement(
        'button',
        {
          class: 'notif-exit-btn'
        },
        'X'
      )
      const confirmBtn = createElement(
        'button',
        {
          class: 'notif-confirm-btn',
          value: asset.dataset.imageId
        },
        'Confirm'
      )

      exitBtn.addEventListener('click', cancel)
      confirmBtn.addEventListener('click', confirm)
      nestElements(searchForOne('.editors'), [
        nestElements(
          createElement('div', {
            class: 'notification',
            'data-linked-image': asset.dataset.imageId
          }),
          [
            createElement(
              'p',
              { class: 'notification-msg' },
              `${json.length - 1} pieces of content will lose ${
                asset.querySelector('p').innerText
              } image\n\nAre you sure you wish to delete it?`
            ),
            exitBtn,
            confirmBtn
          ]
        )
      ])
    }

    const checkForLinkedContent = async (e) => {
      const thisAsset = e.target.closest('.asset-box')
      const request = {
        method: 'POST',
        body: JSON.stringify({
          image_id: parseInt(e.target.closest('button').value)
        }),
        headers: {
          'Content-Type': 'application/json'
        }
      }
      const response = await fetch('/admin/assets/delete', request).then((r) =>
        r.json()
      )

      if (response[0].message === 1) {
        handleNotification(response, thisAsset)
      } else if (response[0].message === 0) {
        await deleteImage(e.target.closest('button'))
      }
    }

    const viewFullImage = (e) => {
      const { 1: thisImage } = e.target.closest('.asset-box').children
      window.open(thisImage.src, '_blank')
    }

    const selectThisContent = (e) => {
      const div = e.currentTarget
      if (searchForOne(`div[data-linked-image="${div.dataset.imageId}"]`))
        return
      const parentDiv = div.parentElement
      parentDiv.querySelectorAll('.selected').forEach((d) => {
        if (d !== div) {
          d.classList.toggle('selected')
          d.querySelector('.asset-box > .btn-group').remove()
        }
      })
      div.classList.toggle('selected')
      if (div.classList[div.classList.length - 1] === 'selected') {
        const deleteBtn = createElement('button', {
          type: 'button',
          value: div.dataset.imageId
        })
        const replaceInput = createElement('input', {
          type: 'file',
          name: 'file',
          'data-image-id': div.dataset.imageId,
          class: 'replace-image',
          autocomplete: 'off',
          onchange: "generateImageEditor(event, 'edit')"
        })
        const replaceBtn = nestElements(
          createElement('label', { class: 'replace' }),
          [
            replaceInput,
            nestElements(
              createElement('div', {
                class: 'replace-image-button',
                value: div.dataset.imageId
              }),
              [
                nestElements(
                  createSVG('svg', null, [112.18, 93.927], ['100%', '100%']),
                  [
                    nestElements(
                      createSVG('g', {
                        transform: 'translate(-17.601098,6.0505133)',
                        fill: 'white',
                        stroke: '#000'
                      }),
                      [
                        createSVG('path', {
                          d: 'm58.876 48.925-40.5-40.5-0.30907 40.809z',
                          'stroke-linecap': 'round',
                          'stroke-linejoin': 'round',
                          'stroke-width': '.5'
                        }),
                        createSVG('path', {
                          d: 'm47.719 36.249s12.557-22.668 49.486-41.671c-40.32 5.2933-66.153 25.004-66.153 25.004z',
                          'stroke-width': '.5'
                        }),
                        createSVG('path', {
                          d: 'm88.326 32.974 40.5 40.5 0.30908-40.809z',
                          'stroke-linecap': 'round',
                          'stroke-linejoin': 'round',
                          'stroke-width': '.5'
                        }),
                        createSVG('path', {
                          d: 'm99.483 45.65s-12.557 22.668-49.486 41.671c40.32-5.2933 66.153-25.004 66.153-25.004z',
                          'stroke-width': '.5'
                        })
                      ]
                    )
                  ]
                )
              ]
            )
          ]
        )
        const previewBtn = nestElements(
          createElement('button', {
            type: 'button'
          }),
          [
            nestElements(
              createSVG('svg', null, [91.81, 44.185], ['100%', '100%']),
              [
                nestElements(
                  createSVG('g', {
                    fill: 'none',
                    stroke: 'white',
                    'stroke-width': '6'
                  }),
                  [
                    createSVG('path', {
                      d: 'm7.0794 17.67c8.009-5.149 26.823-16.598 39.695-16.598 12.872 1.482e-4 30.69 11.449 38.275 16.598 7.5848 5.1489 7.5848 5.6992-1.12e-4 10.404s-25.275 15.038-38.278 15.038c-13.003 1.37e-4 -31.682-10.332-39.691-15.038-8.0091-4.7053-8.0091-5.2557-1.34e-4 -10.405z'
                    }),
                    createSVG('ellipse', {
                      cx: '45.905',
                      cy: '22.093',
                      rx: '14.145',
                      ry: '10.543',
                      'stroke-linecap': 'round',
                      'stroke-linejoin': 'round',
                      fill: 'white',
                      stroke: 'white'
                    })
                  ]
                )
              ]
            )
          ]
        )

        const controls = fragmentElements([
          nestElements(createElement('div', { class: 'btn-group' }), [
            previewBtn,
            replaceBtn,
            nestElements(deleteBtn, [
              nestElements(
                createSVG(
                  'svg',
                  { class: 'trash-can' },
                  [105.83, 119.06],
                  ['100%', '100%']
                ),
                [
                  createSVG('path', {
                    d: 'm22.951 30.289h61.61c0.5235 0 0.99476 0.42382 0.94494 0.94494l-7.4083 77.485c-0.04982 0.52112-5.3265 0.94494-5.85 0.94494h-38.437c-0.5235 0-5.9444-0.42291-5.9836-0.94494l-5.8208-77.485c-0.03922-0.52203 0.42144-0.94494 0.94494-0.94494z',
                    style: 'fill-rule:evenodd;fill:#999;stroke-width:0'
                  }),
                  createSVG('rect', {
                    x: 51.815,
                    y: 49.944,
                    width: 2.0045,
                    height: 44.099,
                    ry: 1.0023,
                    style:
                      'fill-rule:evenodd;fill:#ececec;stroke-width:.265;stroke:#999'
                  }),
                  createSVG('rect', {
                    x: 60.142,
                    y: 48.893,
                    width: 2.0045,
                    height: 44.099,
                    ry: 1.0023,
                    style:
                      'fill-rule:evenodd;fill:#ececec;stroke-width:.265;stroke:#999',
                    transform: 'rotate(1)'
                  }),
                  createSVG('rect', {
                    x: 68.447,
                    y: 47.579,
                    width: 2.0045,
                    height: 44.099,
                    ry: 1.0023,
                    style:
                      'fill-rule:evenodd;fill:#ececec;stroke-width:.265;stroke:#999',
                    transform: 'rotate(2)'
                  }),
                  createSVG('rect', {
                    x: 76.722,
                    y: 46.004,
                    width: 2.0045,
                    height: 44.099,
                    ry: 1.0023,
                    style:
                      'fill-rule:evenodd;fill:#ececec;stroke-width:.265;stroke:#999',
                    transform: 'rotate(3)'
                  }),
                  createSVG('rect', {
                    x: 43.472,
                    y: 50.733,
                    width: 2.0045,
                    height: 44.099,
                    ry: 1.0023,
                    style:
                      'fill-rule:evenodd;fill:#ececec;stroke-width:.265;stroke:#999',
                    transform: 'rotate(-1)'
                  }),
                  createSVG('rect', {
                    x: 35.12,
                    y: 51.26,
                    width: 2.0045,
                    height: 44.099,
                    ry: 1.0023,
                    style:
                      'fill-rule:evenodd;fill:#ececec;stroke-width:.265;stroke:#999',
                    transform: 'rotate(-2)'
                  }),
                  createSVG('rect', {
                    x: 26.764,
                    y: 51.523,
                    width: 2.0045,
                    height: 44.099,
                    ry: 1.0023,
                    style:
                      'fill-rule:evenodd;fill:#ececec;stroke-width:.265;stroke:#999',
                    transform: 'rotate(-3)'
                  }),
                  nestElements(
                    createSVG('g', {
                      class: 'trash-can-lid',
                      transform: 'translate(-.060786 6.35)'
                    }),
                    [
                      createSVG('path', {
                        d: 'm33.872 12.653v-9.472h38.437v9.472',
                        style: 'fill:none;stroke-width:.26458px;stroke:#999'
                      }),
                      createSVG('path', {
                        d: 'm40.128 12.248v-6.0598h25.862v6.0598',
                        style: 'fill:none;stroke-width:.27166;stroke:#999'
                      }),
                      createSVG('path', {
                        d: 'm34.015 8.0121v-4.6771h38.166v9.3543h-6.5619v-6.1471h-25.042v6.1471h-6.5619z',
                        style:
                          'fill-rule:evenodd;fill:#999;stroke-width:.13398;stroke:#999'
                      }),
                      createSVG('rect', {
                        x: 10.093,
                        y: 22.817,
                        width: 85.86,
                        height: 2.0713,
                        style: 'fill-rule:evenodd;fill:#999;stroke-width:0'
                      }),
                      createSVG('rect', {
                        x: 9.9796,
                        y: 12.233,
                        width: 85.86,
                        height: 2.0713,
                        style: 'fill-rule:evenodd;fill:#999;stroke-width:0'
                      }),
                      createSVG('rect', {
                        x: 95.806,
                        y: 12.233,
                        width: 2.0714,
                        height: 12.655,
                        style: 'fill-rule:evenodd;fill:#999;stroke-width:0'
                      }),
                      createSVG('rect', {
                        x: 8.077,
                        y: 12.233,
                        width: 2.0714,
                        height: 12.655,
                        style: 'fill-rule:evenodd;fill:#999;stroke-width:0'
                      }),
                      createSVG('path', {
                        d: 'm10.168 18.561v-4.2256h85.665v8.4513h-85.665z',
                        style:
                          'fill-rule:evenodd;fill:#fff;stroke-width:.034606;stroke:#fff'
                      })
                    ]
                  )
                ]
              )
            ])
          ])
        ])
        deleteBtn.addEventListener('click', checkForLinkedContent)
        // replaceInput.addEventListener('onchange', toggleReplaceForm)
        previewBtn.addEventListener('click', viewFullImage)

        div.prepend(controls)
      } else {
        div.querySelector('.asset-box > .btn-group').remove()
      }
    }

    if (preResponse === null) {
      const response = await fetch('/admin/assets/read').then((r) => r.json())
      content = response
    } else {
      content = preResponse
    }
    empty(imageDisplay)
    content.forEach((c) => {
      const img = createElement('img', {
        class: 'thumbnail',
        src: c.image_link,
        alt: c.image_name
      })
      const assetBox = nestElements(
        createElement('div', {
          class: 'asset-box',
          'data-image-id': c.id
        }),
        [
          fragmentElements([
            img,
            createElement('p', { style: `text-align: right;` }, c.image_name)
          ])
        ]
      )

      assetBox.addEventListener('click', selectThisContent)
      imageDisplay.appendChild(assetBox)
    })
  }

  const generateImageEditor = (e, flag) => {
    const thisInput = e.target
    console.log(thisInput)
    const gate = flag
    const [file] = thisInput.files

    const exitBtn = createElement(
      'button',
      {
        type: 'button',
        class: 'exit-btn'
      },
      'X'
    )

    const boxTitle = createElement(
      'span',
      {
        class: 'box-title'
      },
      gate === 'edit' ? 'Replace Image' : 'Upload New Image'
    )

    const titleBar = nestElements(
      createElement('div', { class: 'title-bar' }),
      [boxTitle, exitBtn]
    )

    const fileNameSpan = createElement('p', { id: 'file-selected' }, file.name)

    const nameLabel = createElement(
      'label',
      { for: 'new-image-name' },
      'New image name'
    )
    const newImageName = createElement('input', {
      type: 'text',
      name: 'new-image-name',
      id: 'new-image-name'
    })
    const uploadButton = createElement(
      'button',
      { class: 'upload-btn' },
      'Upload'
    )

    const displayContainer = nestElements(
      createElement('div', { class: 'display-for-image-info' }),
      [fileNameSpan, nameLabel, newImageName, uploadButton]
    )

    const uploadNewImage = async (e) => {
      const imageEditor = e.target.closest('div.image-uploader')
      const loader = createLoadingSpinner()
      loader.style.cssText = `position: static; transform: translate(0,0);`
      const fd = new FormData()
      if (gate === 'new') {
        fd.append('new_image', file)
        fd.append('image_name', document.querySelector('#new-image-name').value)
      } else if (gate === 'edit') {
        fd.append('new_image', file)
        fd.append('image_name', document.querySelector('#new-image-name').value)
        fd.append('image_id', thisInput.dataset.imageId)
      }
      const url =
        gate === 'edit' ? '/admin/assets/replace' : '/admin/assets/create'
      const request = {
        method: 'POST',
        body: fd
      }
      empty(displayContainer)
      displayContainer.style.cssText = `align-items: center;`
      nestElements(displayContainer, [loader])
      const response = await fetch(url, request).then((r) => r.json())
      exitBtn.click()
      renderImages(response)
    }

    uploadButton.addEventListener('click', uploadNewImage)

    const editNewImageInfo = nestElements(
      createElement('div', { class: 'image-uploader content-editor' }),
      [fragmentElements([titleBar, displayContainer])]
    )

    exitBtn.addEventListener('click', handleExit)

    const existingForms = searchForAll('.editors > .content-editor')
    activeForms = existingForms.length
    dynamicStyles.insertRule(
      `div.form-count${formCount} { transform: matrix(1, 0, 0, 1, -3.37, ${
        activeForms * 35
      }); transition: all 0.2s linear; }`,
      formCount
    )
    dynamicStyles.list.push(formCount)
    console.log('before', dynamicStyles)
    editNewImageInfo.setAttribute('data-form-count', formCount)
    transition(
      'in',
      editNewImageInfo,
      `form-count${formCount}`,
      searchForOne('.editors')
    )
    formCount += 1

    return formCount
  }
</script>

<div id="root">
  <div class="asset-toolbar">
    <label class="input-file-label">
      <input
        class="image-input"
        on:change={(e) => {
          generateImageEditor(e, 'new')
        }}
        type="file"
        name="file"
        id="new-image"
        autocomplete="off"
      />
      <div class="add-image-button">
        <svg
          width="160mm"
          height="160mm"
          version="1.1"
          viewBox="0 0 160 160"
          xmlns="http://www.w3.org/2000/svg"
        >
          <rect
            id="image-icon-sky"
            x="15.62"
            y="13.255"
            width="121.54"
            height="104.12"
            ry="3.4685"
            style="
                  fill-rule: evenodd;
                  fill: #afc6e9;
                  stroke-linejoin: round;
                  stroke-width: 0.30293;
                  stroke: #212178;
                "
          />
          <circle
            id="image-icon-sun"
            cx="101.07"
            cy="41.857"
            r="15"
            style="fill-rule: evenodd; fill: #fea;"
          />
          <path
            id="image-icon-mtn"
            d="m15.567 131.82c-0.1008-0.16133-0.11377-0.97488-0.11377-7.1374 0-5.8751 0.01553-6.9408 0.09998-6.8623 0.11671 0.10862 0.10498 0.12178 3.704-4.1691 14.791-17.635 22.246-26.038 26.561-29.944 3.8555-3.4892 5.7875-3.859 7.9566-1.523 1.9461 2.0959 4.5211 6.4667 9.2052 15.625 0.83247 1.6276 1.6798 3.2246 1.8829 3.5489 0.85286 1.3614 1.681 1.4186 3.099 0.21444 0.72649-0.61698 1.6877-1.6062 5.2984-5.4528 10.832-11.539 16.969-17.668 21.269-21.238 1.7254-1.4326 3.3442-2.4253 4.5288-2.7769 0.78777-0.23384 1.9282-0.25013 2.6309-0.0376 1.5525 0.46951 3.248 1.7671 5.4705 4.1866 4.7051 5.1222 11.446 14.224 25.877 34.94 1.4595 2.0952 2.6811 3.8429 2.7145 3.8838 0.036 0.0439 0.10704 0.0314 0.1736-0.0305 0.10145-0.0944 0.11272 0.73463 0.11272 8.2896 0 8.0284 1.8973 7.0474-0.13364 8.53-2.2066 1.6108-4.4087 0.13557-60.178 0.13557h-60.045z"
            style="
                  fill-rule: evenodd;
                  fill: #212178;
                  stroke-linejoin: round;
                  stroke-width: 0.087734;
                  stroke: #212178;
                "
          />
          <rect
            id="image-icon-frame"
            x="14.252"
            y="11.074"
            width="123.89"
            height="123.89"
            ry="3.644"
            style="
                  fill: none;
                  stroke-linejoin: round;
                  stroke-width: 6.1426;
                  stroke: #000;
                "
          />
          <circle
            cx="114.32"
            cy="117.5"
            r="32.798"
            style="
                  fill-rule: evenodd;
                  fill: #48b748;
                  stroke-linejoin: round;
                  stroke-width: 3.4041;
                  stroke: #48b748;
                "
          />
          <rect
            x="84.347"
            y="112.43"
            width="59.945"
            height="10.129"
            ry="5.0643"
            style="fill-rule: evenodd; fill: #fff; stroke-width: 0;"
          />
          <rect
            transform="rotate(90)"
            x="87.525"
            y="-119.38"
            width="59.945"
            height="10.129"
            ry="5.0643"
            style="fill-rule: evenodd; fill: #fff; stroke-width: 0;"
          />
        </svg>
      </div>
    </label>
  </div>
  <div class="editors" />
  <h1>Images</h1>
  <div id="search-container" class="asset-grid" />
</div>

<style>
  .asset-toolbar {
    /* position: fixed;
  height: 100%; */
    position: fixed;
    height: auto;
    top: auto;
    left: 4px;
    bottom: 4px;
  }

  .editors {
    position: fixed;
    width: clamp(265px, 42vw, 500px);
    z-index: 10;
    box-sizing: border-box;
    top: auto;
    height: 10px;
    right: 1rem;
  }

  .editors > * {
    margin-bottom: 0.5rem;
  }
  .thumbnail {
    width: 80px;
    height: 80px;
    display: block;
  }
  .asset-grid {
    display: grid;
    grid-template-columns: 1fr;
    grid-auto-rows: 1fr;
    gap: 1rem;
    width: 90%;
    margin: 1rem auto 2rem auto;
  }
  .asset-box {
    position: relative;
    padding: 1rem;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .btn-group {
    position: absolute;
    top: 0;
    right: 0;
    display: flex;
    flex-flow: row nowrap;
    width: 100%;
    height: 100%;
    background: var(--light-selected);
    border-radius: 8px;
    justify-content: center;
    align-items: center;
  }
  .btn-group button {
    width: 40px;
    padding: 0.25rem;
    font-size: unset;
    height: 40px;
  }
  input[type='file'] {
    display: none;
  }
  .input-file-label {
    width: 40px;
    display: block;
  }
  div.image-uploader {
    position: absolute;
    top: 0;
    display: flex;
    border-radius: 4px;
    flex-flow: column nowrap;
    width: clamp(320px, 60vw, 480px);
    background: var(--gray);
    z-index: 10;
    transform-box: fill-box;
    transition: all 0.2s linear;
    transform: translate(115%, 0);
    transform-origin: top left;
    right: 0;
    max-height: 432px;
    max-width: 500px;
    box-sizing: border-box;
    padding: 2rem;
  }
  .image-uploader > * {
    margin-bottom: 0.5rem;
  }
  div.display-for-image-info {
    display: flex;
    flex-flow: column nowrap;
    justify-content: center;
    height: 212px;
  }

  input[name='new-image-name'] {
    box-sizing: border-box;
  }
  .image-uploader > *:not(.exit-btn) {
    width: 100%;
  }
  .add-image-button > svg,
  .replace-image-button > svg {
    width: 100%;
    height: auto;
    display: block;
  }
  .add-image-button {
    cursor: pointer;
    padding: 1rem;
    border: 1px solid var(--light);
    width: 100%;
    background: var(--primary);
    border-radius: 4rem;
  }
  .upload-btn {
    margin-top: 1rem;
  }

  .notification {
    position: relative;
    display: flex;
    flex-flow: column nowrap;
    width: clamp(265px, 42vw, 500px);
    border-radius: 4px;
    background: var(--gray);
    transform-box: fill-box;
    transition: all 0.2s linear;
    transform-origin: top left;
    max-height: 432px;
    max-width: 500px;
    align-items: center;
    justify-content: center;
    padding: 1rem;
    box-sizing: border-box;
  }

  .notification-msg {
    text-align: center;
  }

  .notif-exit-btn {
    position: absolute;
    top: 2px;
    right: 2px;
    width: 25px;
    padding: 0.25rem;
    font-size: unset;
    height: 25px;
  }

  label.replace {
    box-sizing: border-box;
    height: 40px;
    padding: 0.25rem;
    width: 40px;
    padding: 0.25rem;
    font-size: unset;
    height: 40px;
    display: block;
    align-content: center;
    justify-content: center;
    background: var(--primary);
    border-radius: 4px;
    border: 0.5px solid var(--light);
  }

  .replace-image-button {
    cursor: pointer;
  }

  .title-bar {
    position: absolute;
    top: 0;
    left: 0;
    display: grid;
    border-radius: 4px 4px 0 0;
    grid-template-rows: 30px;
    grid-template-columns: calc(100% - 44px) 20px 20px;
    width: 100%;
    background: var(--pretty);
    color: black;
  }

  .title-bar > * {
    align-self: center;
  }

  .title-bar > button {
    height: 20px;
    width: 20px;
    display: flex;
    font-size: 15px;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>
