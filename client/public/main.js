const handleScrollDown = (e) => {
  const nextContainer = e.currentTarget.parentElement.nextElementSibling
  nextContainer.scrollIntoView({behavior: 'smooth'})
};
